import sys
import os

import colorama

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.source.document.figure import Figure


class Notebook (Document):


  def __init__ (self, name, path,
                filetype='notebook', reference=None):

    Document.__init__(self, name=name, path=path,
                      filetype=filetype, reference=reference)


  @property
  def filename (self):

    return os.path.basename(self.path[:-1]) + '/' + self.name


  def read (self):

    with open(self.path + self.name, mode='r') as file:
      text = file.read()

    return text


  def get_text_paragraph (self):

    lines = self.read().splitlines()
    raw_text = ' '.join([line for line in lines[1:lines.index('#FIGURES')]])
    text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

    return text


  def get_figs_paragraph (self):

    lines = self.read().splitlines()
    text = '\n'.join([line for line in lines[lines.index('#FIGURES')+1:]])

    return text


  def get_figures (self):

    figlines = self.get_figs_paragraph().splitlines()
    fignames = [line[1:].strip() for line in figlines if line.startswith('-')]
    captions = self.get_fig_captions(figlines)

    figures = [Figure(path=self.path, name=name, caption=cap, reference=self.filename)
               for name, cap in zip(fignames, captions)]

    return figures


  def get_fig_captions (self, figlines):

    captions = []; cap = ''

    for line in figlines:

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


  def check_figs (self):

    missing = [fig.name for fig in self.get_figures()
               if fig.name not in os.listdir(self.path)]

    if missing:
      colorama.init()
      message = 'FAIL: The following files do not exist in the notebook directory:\n\t'
      missing = '\n\t'.join(missing)
      print('>>> \033[91m' + message + '\033[0m' + missing)
      sys.exit()
