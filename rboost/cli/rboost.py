import os
import sys
from datetime import datetime

from plumbum import cli
from tqdm import tqdm
import pandas as pd
import networkx as nx

from rboost.source.gdrive import GDrive
from rboost.source.database import Database
from rboost.source.network import Network

from rboost.utils.autocomplete import AutoComplete


import warnings
warnings.filterwarnings('ignore')


class RBoost (cli.Application):

  PROGNAME = 'rboost'
  VERSION = '0.0.1'

  PATH = os.path.expanduser('~/Desktop/RBoost_Data/').replace('\\', '/')

  pdfs_path      = PATH + 'My_Documents/pdfs/'
  notebooks_path = PATH + 'My_Documents/notebooks/'
  remarks_path   = PATH + 'My_Documents/remarks/'
  downloads_path = PATH + 'My_Downloads/'

  dataframe_columns    = ['DATE', 'USER/AUTHOR', 'DOCNAME', 'DOCTYPE', 'KEYWORDS']
  google_drive_folders = ['pdfs', 'notebooks']

  gdrive = GDrive(client_secrets_file  = PATH + 'client_secrets.json',
                  credentials_file     = PATH + 'credentials.txt',
                  downloads_path       = downloads_path)

  database = Database(filepath = PATH + 'My_Downloads/database.pkl',
                      gdrive   = gdrive)

  network = Network(filepath = PATH + 'My_Downloads/network.pkl',
                    gdrive   = gdrive)

  def main (self):

    if not self.nested_command:
      self.help()

  @property
  def today_date (self):

    today_date = datetime.today().strftime('%d-%m-%Y')

    return today_date

  @property
  def users (self):

    users = set(self.database.dataframe['USER/AUTHOR'])

    return users

  @property
  def docnames (self):

    docnames = set(self.database.dataframe['DOCNAME'])

    return docnames

  @property
  def doctypes (self):

    doctypes = set(self.database.dataframe['DOCTYPE'])

    return doctypes

  @property
  def labnames (self):

    labnames = set(self.network.graph)

    return labnames

  @property
  def labtypes (self):

    labtypes_list = [self.network.graph.nodes[node]['label'].types
                     for node in self.network.graph.nodes]
    labtypes = set().union(*labtypes_list)

    return labtypes

  def get_date (self, auto=False):

    if auto:
      date = self.today_date
    else:
      date = input('>>> Date (dd-mm-yyyy) : ')

    return date

  def get_user (self):

    users = self.users
    with AutoComplete(options=users):
      user = input('>>> User/author (name-surname) : ')

    if user not in users:
      print(f'>>> The user "{user}" does not exist yet on RBoost, do you want to create it?')
      answer = input('>>> (y/n) ')
      if not answer == 'y':
        sys.exit()

    return user

  @staticmethod
  def show_dataframe (df, full=False):

    pd.set_option('colheader_justify', 'right')
    if full:
      pd.set_option('display.max_rows', None)
      pd.set_option('display.max_colwidth', None)

    print(df)

  @staticmethod
  def reset_gdrive ():

    files_list = RBoost.gdrive.service.ListFile().GetList()

    for file in tqdm(files_list, desc='Deleting files', ncols=80):
      file.Delete()

    for foldername in RBoost.google_drive_folders:
      RBoost.gdrive.create_folder(foldername=foldername)

    dataframe = pd.DataFrame(columns=RBoost.dataframe_columns)
    dataframe.to_pickle(RBoost.database.filepath)
    RBoost.gdrive.upload_file(RBoost.database.filepath)
    os.remove(RBoost.database.filepath)

    graph = nx.Graph()
    nx.readwrite.write_gpickle(graph, RBoost.network.filepath)
    RBoost.gdrive.upload_file(RBoost.network.filepath)
    os.remove(RBoost.network.filepath)
