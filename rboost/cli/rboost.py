import os
import datetime

from plumbum import cli
from rboost.cli.__path import PATH



class RBoost (cli.Application):


  PROGNAME = 'rboost'
  VERSION = '0.0.1'


  _pdfs_path      = PATH + '/rboost/database/pdfs/'
  _notebooks_path = PATH + '/rboost/database/notebooks/'
  _remarks_path   = PATH + '/rboost/database/remarks/'

  _database_pkl = PATH + '/rboost/database/pickles/database.pkl'
  _network_pkl  = PATH + '/rboost/database/pickles/network.pkl'


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


  _date = datetime.datetime.today().strftime('%d-%m-%Y')


  def main (self):

    if not self.nested_command:
      os.system('rboost --help')
