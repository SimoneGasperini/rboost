import os
from stat import S_IREAD, S_IWUSR

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Remark (Document):
  """
  Class for the Remark object


  Parameters
  ----------
    path : str
      Remark local path

    name : str
      Remark specific name

    special : str
      Remark special type

    date : str, default=None
      Remark date (dd-mm-yyyy)

    user : str, default=None
      Remark author (name-surname)
  """

  def __init__ (self, path, name, special, date=None, user=None):

    doctype = 'remark-' + special
    name = doctype + '_' + name + '.txt'

    Document.__init__(self,
                      date=date, user=user,
                      path=path, name=name,
                      doctype=doctype)

  @property
  def docname (self):
    """
    Full Remark name (str)
    """

    docname = os.path.basename(self.path[:-1]) + '/' + self.name

    return docname

  def get_text (self):
    """
    Get the pre-processed text extracted from the Remark document


    Returns
    -------
    text : str
      Extracted text
    """

    with open(self.path + self.name, mode='r') as file:
      first_line, raw_text = file.readline(), file.read()

    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text

  def get_data_from_figures (self, figures):
    """
    Raises
    ------
    NotImplementedError
    """

    raise NotImplementedError

  def write_date_and_user (self):
    """
    Write date and user in the first line of the Remark document
    """

    new_line = f'#{self.date}_{self.user}'
    filepath = self.path + self.name

    with open(filepath, mode='r') as file:
      first_line, remainder = file.readline(), file.read()

    os.chmod(filepath, S_IWUSR | S_IREAD)
    with open(filepath, mode='w') as file:
      file.write(new_line + '\n')
      file.write(remainder)
