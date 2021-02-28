import os

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Remark (Document):
  '''
  Class for the Remark object


  Parameters
  ----------
    name : str
      Remark name

    path : str
      Remark local path

    special : str, default='standard'
      Remark special type

    reference : str, default=None
      Name of another Document which the Remark refers to
  '''

  def __init__ (self, name, path, special='standard', reference=None):

    _type = 'remark'
    doctype = _type + ':' + special

    Document.__init__(self, name=name, path=path,
                      doctype=doctype, reference=reference)


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
