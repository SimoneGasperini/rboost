import textract
import colorama

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.cli.rboost import RBoost


class PDF (Document):
  '''
  Class for the PDF document object


  Parameters
  ----------
    name : str
      PDF name

    doctype : str, default='standard'
      PDF type
  '''


  def __init__ (self, name, doctype='standard'):

    path=RBoost._pdfs_path

    Document.__init__(self, name=name, path=path,
                      doctype=doctype, reference=None)


  @property
  def docname (self):
    '''
    Full PDF name (str)
    '''

    docname = self.name

    return docname


  def get_text (self):
    '''
    Get the pre-processed text extracted from the PDF document


    Returns
    -------
    text : str
      Extracted text (None if the extraction fails)
    '''

    try:
      encoded_bytes = textract.process(self.path + self.name)

    except UnicodeDecodeError:
      colorama.init()
      message = f'WARNING: The pdf file "{self.name}" cannot be read'
      print('>>> \033[93m' + message + '\033[0m')
      return None

    raw_text = encoded_bytes.decode('utf-8')
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text


  def open_editor (self):
    '''
    Raises
    ------
    NotImplementedError
    '''

    raise NotImplementedError


  def get_data_from_figures (self, figures):
    '''
    Raises
    ------
    NotImplementedError
    '''

    raise NotImplementedError
