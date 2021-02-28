import os
import sys
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from itertools import combinations

import pandas as pd

import nltk
from gensim import summarization

from rboost.cli.rboost import RBoost


class Document ():
  '''
  Base class for the document object


  Parameters
  ----------
    name : str
      Document name

    path : str
      Document local path

    doctype : str
      Document type

    reference : str
      Name of another Document which the Document refers to
  '''


  def __init__ (self, name, path, doctype, reference):

    self.name = name
    self.path = path
    self.doctype = doctype
    self.reference = reference


  @staticmethod
  def get_keywords (text, doctype):
    '''
    Get the keywords and their score from text according to the RBoost's
    default extraction ratios given by doctype


    Parameters
    ----------
    text : str
      Text to extract the keywords from

    doctype : str
      Origin document doctype of text

    Returns
    -------
    keywords : dict
      Extracted keywords mapped to their score
    '''

    typing = doctype[:6] if doctype.startswith('remark:') else doctype
    ratio = RBoost._keyword_ratios[typing]

    raw_kws = summarization.keywords(text, ratio=ratio, scores=True, lemmatize=True, split=True)

    l = nltk.wordnet.WordNetLemmatizer()
    keywords = {l.lemmatize(word) : round(score,3) for (word, score) in raw_kws}

    return keywords


  def open_editor (self):
    '''
    Open the document using the system's basic text editor


    Raises
    ------
    SystemError
      If the system platform is not supported

    Returns
    -------
    None
    '''

    file = self.path + self.name
    os.chmod(file, S_IWUSR|S_IREAD)

    if sys.platform.startswith('win'):
      os.system('notepad ' + file)
      os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)

    elif sys.platform.startswith('linux'):
      os.system('gedit ' + file)
      os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)

    else:
      raise SystemError('System platform not supported')


  def get_data_from_text (self, text):
    '''
    Get the structured data extracted from text, ready to be used to update
    RBoost's labels network


    Parameters
    ----------
    text : str
      Text to get the data from

    Returns
    -------
    labs : list of dict
      Labels data

    edges : list of tuple
      Links between labels
    '''

    docname = self.docname
    doctype = self.doctype
    labtype = doctype[7:] if doctype.startswith('remark:') else doctype

    keywords = Document.get_keywords(text=text, doctype=doctype)

    labs = [{'name'          : kw,
             'queries_count' : 0,
             'uploads_count' : 1,
             'mentions'      : pd.DataFrame({'DOCNAME' : [docname],
                                             'TYPE'    : [labtype],
                                             'SCORE'   : [keywords[kw]]})
             }
            for kw in keywords
            ]

    edges = list(combinations(keywords.keys(), 2))

    return labs, edges


  def get_data_from_figures (self, figures):
    '''
    Get the structured data extracted from figures, ready to be used to
    update RBoost's labels network


    Parameters
    ----------
    figures : list of Figure
      Figure objects to get the data from

    Returns
    -------
    labs : list of dict
      Labels data

    edges : list of tuple
      Links between labels
    '''

    labs = []; edges = []

    for fig in figures:

      data = fig.get_caption_data()
      if data is None: continue

      new_labs, new_edges = data
      labs += new_labs
      edges += new_edges

    return labs, edges
