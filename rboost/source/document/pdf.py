import textract

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class PDF (Document):


  def __init__ (self, abspath, name, filetype='standard', reference=None):

    path = abspath

    Document.__init__(self,
                      path=path,
                      name=name,
                      filetype=filetype,
                      reference=reference)


  @property
  def filename (self):

    return self.name


  def get_text (self):

    encoded_bytes = textract.process(self.path + self.name)

    raw_text = (encoded_bytes.decode('utf-8'))
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text
