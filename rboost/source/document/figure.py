import os
from itertools import combinations

import pandas as pd

from rboost.source.document.base import Document


class Figure (Document):


  def __init__ (self, name, path,
                caption, filetype='figure', reference=None):

    self.caption = caption

    Document.__init__(self, name=name, path=path,
                      filetype=filetype, reference=reference)


  @property
  def filename (self):

    return os.path.basename(self.path[:-1]) + '/' + self.name


  def get_caption_data (self):

    if self.caption is None: return None    

    filename = self.filename
    filetype = labtype = 'caption'

    keywords = Document.get_keywords(text=self.caption, filetype=filetype)

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
