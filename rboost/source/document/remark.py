import os
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Remark (Document):
  '''
  Class for the Remark object


  Parameters
  ----------
    date : str
      Remark date (dd-mm-yyyy)

    user : str
      Remark author (name-surname)

    path : str
      Remark local path

    name : str
      Remark specific name

    special : str, default='standard'
      Remark special type
  '''

  def __init__ (self, date, user, path, name, special='standard'):

    doctype = 'remark-' + special
    name = doctype + '_' + name + '.txt'

    Document.__init__(self,
                      date=date, user=user,
                      path=path, name=name,
                      doctype=doctype)


  @property
  def docname (self):
    '''
    Full Remark name (str)
    '''

    docname = os.path.basename(self.path[:-1]) + '/' + self.name

    return docname


  def get_text (self):
    '''
    Get the pre-processed text extracted from the Remark document


    Returns
    -------
    text : str
      Extracted text
    '''

    with open(self.path + self.name, mode='r') as file:
      raw_text = file.read()

    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text


  def get_data_from_figures (self, figures):
    '''
    Raises
    ------
    NotImplementedError
    '''

    raise NotImplementedError
