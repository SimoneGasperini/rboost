from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.source.document.figure import Figure


class Notebook (Document):


  def __init__ (self, abspath, dirname, name, filetype='notebook', reference=None):

    if name is None:

      date = input('>>> DATE (dd-mm-yyyy) : ')
      author = input('>>> AUTHOR (name-surname) : ')
      name = date + '_' + author + '.txt'

    path = abspath + dirname + '/'

    self.dirname = dirname

    Document.__init__(self,
                      path=path,
                      name=name,
                      filetype=filetype,
                      reference=reference)


  def __repr__ (self):

    rep = self.filename + '\n\n'
    rep += 'TEXT\n----\n'
    rep += self.get_text() + '\n\n'

    rep += 'FIGURES\n-------\n'
    for fig in self.get_figures():
      rep += fig.__repr__() + '\n'

    return rep


  @property
  def filename (self):

    return self.dirname + '/' + self.name


  def create_new (self):

    with open(self.path + self.name, mode='w') as file:
      file.write('#TEXT\n\n\n#FIGURES\n\n\n')


  def read_lines (self):

    with open(self.path + self.name, mode='r') as file:
      lines = file.read().splitlines()

    return lines


  def get_text (self):

    lines = self.read_lines()
    raw_text = ' '.join([line for line in lines[1:lines.index('#FIGURES')]])
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text


  def get_figures (self):

    lines = self.read_lines()
    figlines = [line for line in lines[lines.index('#FIGURES')+1:]]

    fignames = [line[1:] for line in figlines if line.startswith('-')]
    captions = self.get_fig_captions(figlines)

    figures = [Figure(abspath=self.path, dirname=self.dirname,
                      name=name, caption=cap, reference=self.filename)
               for name, cap in zip(fignames, captions)]

    return figures


  def get_fig_captions (self, figlines):

    captions = []; cap = None

    for line in figlines:

      if line == '': continue

      if line.startswith('-'):
        if cap is not None: captions.append(cap)
        cap = ''

      else:
        cap = cap + ' ' + line

    captions.append(cap)
    captions = [strip_non_alphanum(strip_punctuation(cap.lower()))
                if not cap == '' else None
                for cap in captions]

    return captions



if __name__ == '__main__':

  notebook = Notebook(abspath='../../database/notebooks/',
                      dirname='photonic_crystals',
                      name='23-02-2021_Enrico-Tartari.txt')

  print(notebook)
