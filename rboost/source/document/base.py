from itertools import combinations
import pandas as pd
import nltk
from gensim import summarization

from rboost.cli.rboost import RBoost


class Document:
  """
  Abstract base class for the document object


  Parameters
  ----------
    date : str
      Document date (dd-mm-yyyy)

    user : str
      Document author/user (name-surname)

    path : str
      Document local path

    name : str
      Document name

    doctype : str
      Document type
  """

  def __init__ (self, date, user, path, name, doctype):

    self.date = date
    self.user = user
    self.path = path
    self.name = name
    self.doctype = doctype

    if doctype == 'notebook' or doctype.startswith('remark-'):
      self.open_editor()

    self.text = self.caption if doctype == 'figure' else self.get_text()
    self.keywords = self.get_keywords()

  def get_keywords (self):
    """
    Get the keywords and their score from text according to the RBoost's
    default extraction ratios given by the document type

    Returns
    -------
    keywords : dict
      Extracted keywords mapped to their score
    """

    if self.text is None:
      return {}

    typing = self.doctype.split('-')[0]
    ratio = RBoost.keyword_ratios[typing]

    raw_kws = summarization.keywords(self.text, ratio=ratio, scores=True, lemmatize=True, split=True)

    lmt = nltk.wordnet.WordNetLemmatizer()
    keywords = {lmt.lemmatize(word): round(score, 3) for (word, score) in raw_kws}

    return keywords

  def get_data_from_text (self):
    """
    Get the structured data extracted from text, ready to be used to update
    RBoost's labels network


    Returns
    -------
    labs : list of dict
      Labels data

    edges : list of tuple
      Links between labels
    """

    labtype = self.doctype.split('-')[1] if self.doctype.startswith('remark-') else self.doctype

    labs = [{'name'          : kw,
             'queries_count' : 0,
             'uploads_count' : 1,
             'mentions'      : pd.DataFrame({'DOCNAME' : [self.docname],
                                             'TYPE'    : [labtype],
                                             'SCORE'   : [self.keywords[kw]]})
             }
            for kw in self.keywords
            ]

    edges = list(combinations(self.keywords.keys(), 2))

    return labs, edges

  def get_data_from_figures (self):
    """
    Get the structured data extracted from figures, ready to be used to
    update RBoost's labels network


    Returns
    -------
    labs : list of dict
      Labels data

    edges : list of tuple
      Links between labels
    """

    labs = []
    edges = []

    for fig in self.figures:

      data = fig.get_data_from_text()
      if data is None:
        continue

      new_labs, new_edges = data
      labs += new_labs
      edges += new_edges

    return labs, edges
