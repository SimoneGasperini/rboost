import os
from datetime import datetime

from plumbum import cli

from rboost.source.gdrive import GDrive


class RBoost (cli.Application):


  PROGNAME = 'rboost'
  VERSION = '0.0.1'

  PATH = os.path.expanduser('~/Desktop/RBoost_Data').replace('\\','/')


  _pdfs_path = PATH + '/My_Documents/pdfs/'
  _notebooks_path = PATH + '/My_Documents/notebooks/'
  _remarks_path = PATH + '/My_Documents/remarks/'

  _database_pkl = PATH + '/My_Downloads/database.pkl'
  _network_pkl  = PATH + '/My_Downloads/network.pkl'
  _downloads_path = PATH + '/My_Downloads/'

  _gdrive_path = PATH + '/client_token/'
  _gdrive_folders = ['notebook','pdfs','remarks']

  gdrive = GDrive(_gdrive_path, _gdrive_folders,
                  _database_pkl, _network_pkl, _downloads_path)


  _remark_types = ['standard',
                   'problem',
                   'solution',
                   'technique',
                   'reasoning',
                   'note']

  _document_types = ['standard',
                     'notebook',
                     'figure'] + ['remark:' + t
                                   for t in _remark_types]

  _keyword_ratios = {'standard' : 0.01,
                     'notebook' : 0.1,
                     'caption'  : 0.6,
                     'remark'   : 0.6}

  _date = datetime.today().strftime('%d-%m-%Y')



  def main (self):

    if not self.nested_command:
      os.system('rboost --help')
