import os
import sys
import pandas as pd
from tqdm import tqdm

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.notebook import Notebook
from rboost.utils.exception import RBException


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
    path = RBoost._notebooks_path + dirname + '/'

    notebook = Notebook(date=date, user=author, path=path)
    self.create_file(notebook)

    notebook.open_editor()
    notebook.check_figures()

    figures = notebook.get_figures()
    self.upload_files(notebook, figures)

    self.update_database(notebook, figures)
    self.update_network(notebook, figures)


  @staticmethod
  def create_dir (dirname):

    dirpath = RBoost._notebooks_path + dirname

    if os.path.exists(dirpath):
      print(f'>>> The notebook "{dirname}" already exists, do you want to add a page?')
      answer = input('>>> (y/n) ')
      if not answer == 'y':
        sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" does not exist yet, do you want to create it?')
      answer = input('>>> (y/n) ')
      if answer == 'y':
        os.makedirs(dirpath)
      else:
        sys.exit()


  @staticmethod
  def create_file (notebook):

    with Database() as db:

      if notebook.docname in db.dataframe['DOCNAME'].tolist():
        RBException(state='failure',
                    message=f'The file "{notebook.docname}" already exists in RBoost database')

    if notebook.name not in os.listdir(notebook.path):
      with open(notebook.path + notebook.name, mode='w') as file:
        file.write('#TEXT\n\n#FIGURES\n\n')


  @staticmethod
  def upload_files (notebook, figures):

    print(f'>>> Do you want to upload the file "{notebook.docname}" on RBoost database?')
    answer = input('>>> (y/n) ')
    if not answer == 'y':
      sys.exit()

    print(f'>>> Uploading "{notebook.docname}"')

    folder = notebook.docname.split('/')[0]
    RBoost.gdrive.create_folder(foldername=folder, parent_folder='notebooks')

    filepaths = [notebook.path + notebook.name] + [fig.path + fig.name for fig in figures]

    for filepath in tqdm(filepaths, desc='Uploading files', ncols=80):
      RBoost.gdrive.upload_file(filepath=filepath, parent_folder=folder)


  @staticmethod
  def update_database (notebook, figures):

    with Database() as db:

      data = [[fig.date, fig.user, fig.docname, fig.doctype]
              for fig in figures]
      data.append([notebook.date, notebook.user, notebook.docname, notebook.doctype])

      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)


  @staticmethod
  def update_network (notebook, figures):

    text = notebook.get_text()

    with Network() as net:

      text_labs, text_links = notebook.get_data_from_text(text)
      figs_labs, figs_links = notebook.get_data_from_figures(figures)

      net.update_nodes(text_labs + figs_labs)
      net.update_edges(text_links + figs_links)
