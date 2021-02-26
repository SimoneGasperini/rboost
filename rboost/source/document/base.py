from itertools import combinations

import pandas as pd

import nltk
from gensim.summarization import keywords


class Document ():

  keywords_ratio = {'standard' : 0.01,
                    'notebook' : 0.1,
                    'caption'  : None,
                    'remark'   : 0.6}

  keywords_num = {'standard' : None,
                  'notebook' : None,
                  'caption'  : 2,
                  'remark'   : None}


  def __init__ (self, path, name, filetype, reference):

    self.path = path
    self.name = name
    self.filetype = filetype
    self.reference = reference


  @staticmethod
  def get_keywords (text, typing):

    ratio = Document.keywords_ratio[typing]
    words = Document.keywords_num[typing]

    raw_kws = keywords(text, ratio=ratio, words=words,
                       scores=True, lemmatize=True, split=True)

    l = nltk.wordnet.WordNetLemmatizer()
    kws = {l.lemmatize(word) : round(score,3) for (word, score) in raw_kws}

    return kws


  def get_data_from_text (self, text):

    filename = self.filename
    typing = self.filetype

    keywords = Document.get_keywords(text=text, typing=typing)

    labs = [{'name'          : kw,
             'queries_count' : 0,
             'uploads_count' : 1,
             'mentions'      : pd.DataFrame({'FILENAME' : [filename],
                                             'FILETYPE' : [typing],
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
