from itertools import combinations

import pandas as pd

from rboost.source.document.base import Document


class Figure (Document):


  def __init__ (self, abspath, dirname, name, caption, filetype='figure', reference=None):

    path = abspath

    self.dirname = dirname
    self.caption = caption

    Document.__init__(self,
                      path=path,
                      name=name,
                      filetype=filetype,
                      reference=reference)


  def __repr__ (self):

    return f'{self.filename}\n{self.caption}\n'


  @property
  def filename (self):

    return self.dirname + '/' + self.name


  def get_caption_data (self):

    if self.caption is None: return None    

    filename = self.filename
    typing = 'caption'

    keywords = Document.get_keywords(text=self.caption, typing=typing)

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
