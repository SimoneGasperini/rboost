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

  nb_path = RBoost.PATH + '/rboost/database/notebooks/'
  pickle_path = RBoost.PATH + '/rboost/database/pickles/'


  def main (self, dirname):

    self.check_dir(dirname=dirname)
    os.makedirs(self.nb_path + dirname, exist_ok=True)

    notebook = self.create_file(dirname=dirname)
    os.system('notepad ' + notebook.path + notebook.name)

    self.check_refs(notebook)
    self.upload_file(notebook)


  def check_dir (self, dirname):

    if os.path.exists(self.nb_path + dirname):
      print(f'>>> The notebook "{dirname}" already exists, do you want to update it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" does not exist yet, do you want to create it?')
      if not input('>>> (y/n) ') == 'y': sys.exit()


  def create_file (self, dirname):

    notebook = Notebook(path=self.nb_path, dirname=dirname)

    with Database(path=self.pickle_path, name='database.pkl') as db:

      if dirname + '/' + notebook.name in list(db.df['FILENAME']):
        colorama.init()
        message = f'--> FAIL: The file "{notebook.name}" already exists in RBoost database'
        print('\033[91m' + message + '\033[0m')
        sys.exit()

    if notebook.name not in os.listdir(self.nb_path + dirname):
      notebook.create_new()

    return notebook


  def check_refs (self, notebook):

    lines = notebook.read_lines()

    images = [line[1:] for line in lines[lines.index('#IMAGES')+1:] if line.startswith('-')]
    not_found = [img for img in images if img not in os.listdir(notebook.path)]

    if not_found:
      colorama.init()
      message = '--> FAIL: The following images files do not exist:\n\t' + '\n\t'.join(not_found)
      print('\033[91m' + message + '\033[0m')
      sys.exit()


  def upload_file (self, notebook):

    filename = os.path.basename(notebook.path[:-1]) + '/' + notebook.name
    print(f'>>> Are you sure to upload the file "{filename}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'Uploading "{filename}"')

    with Database(path=self.pickle_path, name='database.pkl') as db:

      data = [[filename, notebook.filetype, notebook.name[:10]]]
      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)

    with Network(path=self.pickle_path, name='network.pkl') as net:

      labsinfo, relations = notebook.get_data()
      net.update_nodes(labsinfo)
      net.update_edges(relations)
