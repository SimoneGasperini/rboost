import os
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.cli.rboost import RBoost
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

    topic : str
      Remark topic name

    special : str, default='standard'
      Remark special type

    reference : str, default=None
      Name of another Document which the Remark refers to
  '''

  def __init__ (self, date, user, topic, special='standard', reference=None):

    path = RBoost._remarks_path + reference + '/'
    name = date + '_' + user + '_' + topic + '.txt'
    doctype = 'remark:' + special

    Document.__init__(self, date, user, path, name, doctype, reference)


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
