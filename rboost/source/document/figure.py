import os
from itertools import combinations

import pandas as pd

from rboost.source.document.base import Document


class Figure ():
  '''
  Class for the Figure object


  Parameters
  ----------
    name : str
      Figure name

    path : str
      Figure local path

    caption : str, default=None
      Figure caption

    reference : str, default=None
      Name of another Document where a reference to the Figure is contained
  '''

  def __init__ (self, name, path, caption=None, reference=None):

    self.name = name
    self.path = path
    self.doctype = 'figure'
    self.caption = caption
    self.reference = reference


  @property
  def docname (self):
    '''
    Full Figure name (str)
    '''

    docname = os.path.basename(self.path[:-1]) + '/' + self.name

    return docname


  def get_caption_data (self):
    '''
    Get the structured data extracted from the Figure caption, ready to be
    used to update RBoost's labels network


    Returns
    -------
    labs : list of dict
      Labels data (None if the caption is None)

    edges : list of tuple
      Links between labels (None if the caption is None)
    '''

    if self.caption is None: return None

    docname = self.docname
    doctype = labtype = 'caption'

    keywords = Document.get_keywords(text=self.caption, doctype=doctype)

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
