import os

from plumbum import cli

from rboost.drive.gdrive import GDrive
from rboost.cli.__path import PATH


class RBoost (cli.Application):


  PROGNAME = 'rboost'
  VERSION = '0.0.1'


  _gdrive_path = PATH + '/rboost/rboost/drive/'
  _gdrive_folders = ['notebook','pdfs','remarks']

  _pdfs_path = PATH + '/RBoost_Data/My_Documents/pdfs/'
  _notebooks_path = PATH + '/RBoost_Data/My_Documents/notebooks/'
  _remarks_path = PATH + '/RBoost_Data/My_Documents/remarks/'

  _database_pkl = PATH + '/RBoost_Data/My_Downloads/database.pkl'
  _network_pkl  = PATH + '/RBoost_Data/My_Downloads/network.pkl'
  _downloads_path = PATH + '/RBoost_Data/My_Downloads/'

  gdrive = GDrive(_gdrive_path, _gdrive_folders,
                  _database_pkl, _network_pkl,
                  _downloads_path)


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



  def main (self):

    if not self.nested_command:
      os.system('rboost --help')
