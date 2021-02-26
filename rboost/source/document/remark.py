from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Remark (Document):


  def __init__ (self, abspath, dirname, filetype='remark', special=None, date=None, reference=None):

    path = abspath + dirname + '/'
    name = special + '_' + date + '.txt'
    filetype = filetype + ':' + special

    self.dirname = dirname
    self.special = special

    Document.__init__(self,
                      path=path,
                      name=name,
                      filetype=filetype,
                      reference=reference)


  @property
  def filename (self):

    return self.dirname + '/' + self.name


  def get_text (self):

    with open(self.path + self.name, mode='r') as file:
      raw_text = file.read()

    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text
