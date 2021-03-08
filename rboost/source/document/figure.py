import os
from itertools import combinations

import pandas as pd

from rboost.source.document.base import Document


class Figure ():
  '''
  Class for the Figure object


  Parameters
  ----------
    date : str
      Figure date (dd-mm-yyyy)

    user : str
      Figure author/user (name-surname)

    path : str
      Figure local path

    name : str
      Figure name

    caption : str, default=None
      Figure caption

    reference : str, default=None
      Name of another Document where a reference to the Figure is contained
  '''

  def __init__ (self, date, user, path, name, caption=None, reference=None):

    self.date = date
    self.user = user
    self.path = path
    self.name = name
    self.caption = caption
    self.reference = reference

    self.doctype = 'figure'


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
