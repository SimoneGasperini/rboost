import os
import sys

import pandas as pd
import colorama

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.notebook import Notebook


@RBoost.subcommand ('write-notebook')
class WriteNotebook (RBoost):
  '''
  Write a notebook on RBoost database
  '''


  def main (self, dirname):

    self.check_dir(dirname=dirname)
    os.makedirs(self.notebooks_path + dirname, exist_ok=True)

    notebook = self.create_file(dirname)
    self.open_editor(notebook)

    self.check_refs(notebook)
    self.upload_file(notebook)


  def check_dir (self, dirname):

    if os.path.exists(self.notebooks_path + dirname):
      print(f'>>> The notebook "{dirname}" already exists, do you want to update it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" does not exist yet, do you want to create it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()


  def create_file (self, dirname):

    notebook = Notebook(abspath=self.notebooks_path, dirname=dirname)

    with Database() as db:

      if notebook.filename in list(db.df['FILENAME']):
        colorama.init()
        message = f'FAIL: The file "{notebook.name}" already exists in RBoost database'
        print('>>> \033[91m' + message + '\033[0m')
        sys.exit()

    if notebook.name not in os.listdir(self.notebooks_path + dirname):
      notebook.create_new()

    return notebook


  def open_editor (self, notebook):

    if sys.platform.startswith('win'):
      os.system('notepad ' + notebook.path + notebook.name)

    elif sys.platform.startswith('linux'):
      os.system('gedit ' + notebook.path + notebook.name)

    else:
      raise SystemError


  def check_refs (self, notebook):

    lines = notebook.read_lines()

    images = [line[1:] for line in lines[lines.index('#FIGURES')+1:] if line.startswith('-')]
    not_found = [img for img in images if img not in os.listdir(notebook.path)]

    if not_found:
      colorama.init()
      message = 'FAIL: The following files do not exist in the notebook directory:\n\t'
      figures = '\n\t'.join(not_found)
      print('>>> \033[91m' + message + '\033[0m' + figures)
      sys.exit()


  def upload_file (self, notebook):

    print(f'>>> Are you sure to upload the file "{notebook.filename}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'>>> Uploading "{notebook.filename}"')

    date = notebook.name[:10]
    text = notebook.get_text()
    figures = notebook.get_figures()

    with Database() as db:

      data = [[date, fig.filename, fig.filetype, fig.reference] for fig in figures]
      data.append([date, notebook.filename, notebook.filetype, notebook.reference])
      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)

    with Network() as net:

      text_labs, text_links = notebook.get_data_from_text(text)
      figs_labs, figs_links = notebook.get_data_from_figures(figures)
      net.update_nodes(text_labs + figs_labs)
      net.update_edges(text_links + figs_links)
