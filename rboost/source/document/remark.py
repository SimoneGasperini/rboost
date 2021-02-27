import os

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Remark (Document):


  def __init__ (self, name, path,
                special='standard', filetype='remark', reference=None):

    filetype = filetype + ':' + special

    Document.__init__(self, name=name, path=path,
                      filetype=filetype, reference=reference)


  @property
  def filename (self):

    return os.path.basename(self.path[:-1]) + '/' + self.name


  def get_text (self):

    with open(self.path + self.name, mode='r') as file:
      raw_text = file.read()

    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text
