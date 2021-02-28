import os
import sys
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

import colorama
import pandas as pd

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

    dirpath = self._notebooks_path + dirname + '/'

    self.check_dir(dirpath)
    os.makedirs(dirpath, exist_ok=True)

    notebook = Notebook(path=dirpath, name=self.get_name())
    self.check_file(notebook)

    notebook.open_editor()
    notebook.check_figs()

    self.upload_file(notebook)
    self.update_document(dirname, notebook)


  @staticmethod
  def check_dir (dirpath):

    dirname = os.path.basename(dirpath[:-1])

    if os.path.exists(dirpath):
      print(f'>>> The notebook "{dirname}" already exists, do you want to add a page?')
      if not input('>>> (y/n) ') == 'y': sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" does not exist yet, do you want to create it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()


  @staticmethod
  def get_name ():

    date = input('>>> Date (dd-mm-yyyy) : ')
    author = input('>>> Author (name-surname) : ')
    name = date + '_' + author + '.txt'

    return name


  @staticmethod
  def check_file (notebook):

    with Database() as db:

      if notebook.docname in list(db.df['DOCNAME']):
        colorama.init()
        message = f'FAIL: The file "{notebook.docname}" already exists in RBoost database'
        print('>>> \033[91m' + message + '\033[0m')
        sys.exit()

    if notebook.name not in os.listdir(notebook.path):
      with open(notebook.path + notebook.name, mode='w') as file:
        file.write('#TEXT\n\n#FIGURES\n\n')


  @staticmethod
  def upload_file (notebook):

    print(f'>>> Are you sure to upload the file "{notebook.docname}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'>>> Uploading "{notebook.docname}"')
    text = notebook.get_text_paragraph()
    figures = notebook.get_figures()

    with Database() as db:

      date = notebook.name[:10]
      data = [[date, fig.docname, fig.doctype, fig.reference] for fig in figures]
      data.append([date, notebook.docname, notebook.doctype, notebook.reference])
      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)

    with Network() as net:

      text_labs, text_links = notebook.get_data_from_text(text)
      figs_labs, figs_links = notebook.get_data_from_figures(figures)
      net.update_nodes(text_labs + figs_labs)
      net.update_edges(text_links + figs_links)


  @staticmethod
  def update_document (dirname, notebook):

    dirpath = RBoost._notebooks_path + dirname + '/'
    docname = dirname + '.txt'

    title = notebook.name + '\n' + ('-' * len(notebook.name)) + '\n'
    text = notebook.read()
    separator = ('\n' * 4) + (('#'*100 + '\n') * 2) + ('\n' * 3)

    if docname in os.listdir(dirpath):
      os.chmod(dirpath + docname, S_IWUSR|S_IREAD)

    with open(dirpath + docname, mode='a') as doc:
      doc.write(title + text + separator)

    os.chmod(dirpath + docname, S_IREAD|S_IRGRP|S_IROTH)
