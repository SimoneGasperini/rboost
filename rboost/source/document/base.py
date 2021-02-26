from itertools import combinations

import pandas as pd

import nltk
from gensim.summarization import keywords


class Document ():

  keywords_ratio = {'standard' : 0.01,
                    'notebook' : 0.1,
                    'caption'  : 0.6,
                    'remark'   : 0.6}


  def __init__ (self, path, name, filetype, reference):

    self.path = path
    self.name = name
    self.filetype = filetype
    self.reference = reference


  @staticmethod
  def get_keywords (text, filetype):

    typing = filetype[:6] if filetype.startswith('remark:') else filetype
    ratio = Document.keywords_ratio[typing]

    raw_kws = keywords(text, ratio=ratio, scores=True, lemmatize=True, split=True)

    l = nltk.wordnet.WordNetLemmatizer()
    kws = {l.lemmatize(word) : round(score,3) for (word, score) in raw_kws}

    return kws


  def get_data_from_text (self, text):

    filename = self.filename
    filetype = self.filetype
    labtype = filetype[7:] if filetype.startswith('remark:') else filetype

    keywords = Document.get_keywords(text=text, filetype=filetype)

    labs = [{'name'          : kw,
             'queries_count' : 0,
             'uploads_count' : 1,
             'mentions'      : pd.DataFrame({'FILENAME' : [filename],
                                             'TYPE'     : [labtype],
                                             'SCORE'    : [keywords[kw]]})
             }
            for kw in keywords
            ]

    edges = list(combinations(keywords.keys(), 2))

    return labs, edges


  def get_data_from_figures (self, figures):

    labs = []; edges = []

    for fig in figures:

      data = fig.get_caption_data()
      if data is None: continue

      new_labs, new_edges = data
      labs += new_labs
      edges += new_edges

    return labs, edges
