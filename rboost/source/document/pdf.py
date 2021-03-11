from io import StringIO
from tqdm import tqdm

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.utils.exception import RBException


class PDF (Document):
  '''
  Class for the PDF document object


  Parameters
  ----------
    date : str (dd-mm-yyyy)
      PDF upload date

    user : str
      PDF upload user (name-surname)

    path : str
      PDF local path

    name : str
      PDF name
  '''

  def __init__ (self, date, user, path, name):

    doctype = 'standard'

    Document.__init__(self,
                      date=date, user=user,
                      path=path, name=name,
                      doctype=doctype)


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
      RBException(state='warning', message=f'The pdf file "{self.name}" cannot be read')
      return

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
