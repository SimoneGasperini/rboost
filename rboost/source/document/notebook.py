from itertools import combinations

import pandas as pd

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document


class Notebook (Document):


  def __init__ (self, path, dirname=None, name=None, filetype='notebook'):

    date = input('>>> DATE (dd-mm-yyyy) : ')
    author = input('>>> AUTHOR (name-surname) : ')
    name = date + '_' + author + '.txt'

    path = path + dirname + '/'
    self.dirname = dirname

    Document.__init__(self, path=path, name=name, filetype=filetype)


  def create_new (self):

    with open(self.path + self.name, mode='w') as file:
      file.write('#TEXT\n\n\n#IMAGES\n\n\n')


  def read_lines (self):

    with open(self.path + self.name, mode='r') as file:
      lines = file.read().splitlines()

    return lines


  def get_text (self):

    lines = self.read_lines()
    lines.remove('#TEXT')

    raw_text = ' '.join([line for line in lines[:lines.index('#IMAGES')]])
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text


  def get_data (self):

    filename = self.dirname + '/' + self.name
    filetype = self.filetype
    keywords = self.get_keywords(self.get_text(), ratio=0.2)

    labsinfo = [{'name'          : kw,
                 'query_count'   : 0,
                 'reading_count' : 0,
                 'writing_count' : 1,
                 'mentions'      : pd.DataFrame({'FILENAME' : [filename],
                                                 'FILETYPE' : [filetype],
                                                 'SCORE'    : [keywords[kw]]})
                 }
                for kw in keywords
                ]
    edges = list(combinations(keywords.keys(), 2))

    return labsinfo, edges
