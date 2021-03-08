import os
import sys
from stat import S_IREAD, S_IWUSR

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


  def main (self):

    dirname = input('>>> Notebook name : ')
    self.create_dir(dirname)

    date = input('>>> Date (dd-mm-yyyy) : ')
    author = input('>>> Author (name-surname) : ')

    notebook = Notebook(dirname=dirname, date=date, user=author)
    self.create_file(notebook)

    notebook.open_editor()
    notebook.check_figs()

    self.upload_file(notebook)
    self.update_document(dirname, notebook)


  @staticmethod
  def create_dir (dirname):

    dirpath = RBoost._notebooks_path + dirname

    if os.path.exists(dirpath):
      print(f'>>> The notebook "{dirname}" already exists, do you want to add a page?')
      if not input('>>> (y/n) ') == 'y': sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" does not exist yet, do you want to create it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()

    os.makedirs(dirpath, exist_ok=True)


  @staticmethod
  def create_file (notebook):

    with Database() as db:

      if notebook.docname in db.dataframe['DOCNAME'].tolist():
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

      data = [[fig.date, fig.user, fig.docname, fig.doctype, fig.reference]
              for fig in figures]
      data.append([notebook.date, notebook.user, notebook.docname, notebook.doctype, notebook.reference])
      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)

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

    os.chmod(dirpath + docname, S_IREAD)
