import os
from datetime import datetime
from plumbum import cli

from rboost.source.gdrive import GDrive


class RBoost (cli.Application):


  PROGNAME = 'rboost'
  VERSION = '0.0.1'

  PATH = os.path.expanduser('~/Desktop/RBoost_Data/').replace('\\','/')

  _pdfs_path      = PATH + 'My_Documents/pdfs/'
  _notebooks_path = PATH + 'My_Documents/notebooks/'
  _remarks_path   = PATH + 'My_Documents/remarks/'
  _downloads_path = PATH + 'My_Downloads/'

  _database_pkl   = PATH + 'My_Downloads/database.pkl'
  _network_pkl    = PATH + 'My_Downloads/network.pkl'

  gdrive = GDrive(client_secrets_file  = PATH + 'client_secrets.json',
                  credentials_file     = PATH + 'credentials.txt',
                  gd_folders           = ['pdfs','notebooks'],
                  downloads_path       = _downloads_path,
                  database_pkl         = _database_pkl,
                  network_pkl          = _network_pkl)

  _document_types = ['standard',
                     'notebook',
                     'figure',
                     'remark']

  _keyword_ratios = {'standard' : 0.02,
                     'notebook' : 0.2,
                     'caption'  : 0.6,
                     'remark'   : 0.6}

  _date = datetime.today().strftime('%d-%m-%Y')



  def main (self):

    if not self.nested_command:
      os.system('rboost --help')
