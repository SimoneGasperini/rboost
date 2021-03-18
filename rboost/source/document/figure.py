import os
from abc import ABC

from rboost.source.document.base import Document


class Figure (Document, ABC):
  """
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
  """

  def __init__ (self, date, user, path, name, caption=None):

    doctype = 'figure'
    self.caption = caption

    super(Figure, self).__init__(date=date, user=user,
                                 path=path, name=name,
                                 doctype=doctype)

  @property
  def docname (self):
    """
    Full Figure name (str)
    """

    docname = os.path.basename(self.path[:-1]) + '/' + self.name

    return docname
