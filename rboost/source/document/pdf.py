from itertools import combinations

import textract
import colorama
import pandas as pd

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class PDF (Document):


  def __init__ (self, path, name, filetype='standard'):

    Document.__init__(self, path=path, name=name, filetype=filetype)


  def get_text (self):

    try:
      encoded_bytes = textract.process(self.path + self.name)

    except UnicodeDecodeError:
      colorama.init()
      message = f'--> WARNING: The file "{self.name}" cannot be read'
      print('\033[93m' + message + '\033[0m')
      self.state = False

    else:
      raw_text = (encoded_bytes.decode('utf-8'))
      text = strip_non_alphanum(strip_punctuation(raw_text.lower()))
      return text


  def get_data (self):

    filename = self.name
    filetype = self.filetype
    keywords = self.get_keywords(self.get_text(), ratio=0.01)

    if not self.state:
      return None

    labsinfo = [{'name'          : kw,
                 'query_count'   : 0,
                 'reading_count' : 1,
                 'writing_count' : 0,
                 'mentions'      : pd.DataFrame({'FILENAME' : [filename],
                                                 'FILETYPE' : [filetype],
                                                 'SCORE'    : [keywords[kw]]})
                 }
                for kw in keywords
                ]
    edges = list(combinations(keywords.keys(), 2))

    return labsinfo, edges
