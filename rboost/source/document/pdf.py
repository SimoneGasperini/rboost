import textract
import colorama

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.cli.rboost import RBoost


class PDF (Document):


  def __init__ (self, name, path=RBoost._pdfs_path,
                filetype='standard', reference=None):

    Document.__init__(self, name=name, path=path,
                      filetype=filetype, reference=reference)


  @property
  def filename (self):

    return self.name


  def get_text (self):

    try:
      encoded_bytes = textract.process(self.path + self.name)

    except UnicodeDecodeError:
      colorama.init()
      message = f'WARNING: The file "{self.name}" cannot be read'
      print('>>> \033[93m' + message + '\033[0m')
      return None

    raw_text = encoded_bytes.decode('utf-8')
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text
