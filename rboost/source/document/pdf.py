from io import StringIO

from tqdm import tqdm
import colorama

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.cli.rboost import RBoost


class PDF (Document):
  '''
  Class for the PDF document object


  Parameters
  ----------
    user : str
      PDF user (name-surname)

    name : str
      PDF name

    doctype : str, default='standard'
      PDF type
  '''

  def __init__ (self, user, name, doctype='standard'):

    date = RBoost._date
    path = RBoost._pdfs_path
    reference = None

    Document.__init__(self, date, user, path, name, doctype, reference)


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

    output_string = StringIO()

    try:
      with open(self.path + self.name, 'rb') as file:
        document = PDFDocument(PDFParser(file))
        resource_manager = PDFResourceManager()
        device = TextConverter(resource_manager,
                               output_string,
                               laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in tqdm(list(PDFPage.create_pages(document)), ncols=80):
          interpreter.process_page(page)

    except Exception:
      colorama.init()
      message = f'WARNING: The pdf file "{self.name}" cannot be read'
      print('>>> \033[93m' + message + '\033[0m')
      return None

    text = output_string.getvalue()
    text = strip_non_alphanum(strip_punctuation(text.lower()))

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
