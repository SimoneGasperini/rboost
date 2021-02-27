import os
import datetime

from plumbum import cli
from rboost.cli.__path import PATH



class RBoost (cli.Application):


  PROGNAME = 'rboost'
  VERSION = '0.0.1'


  pdfs_path      = PATH + '/rboost/database/pdfs/'
  notebooks_path = PATH + '/rboost/database/notebooks/'
  remarks_path   = PATH + '/rboost/database/remarks/'

  database_pkl = PATH + '/rboost/database/pickles/database.pkl'
  network_pkl  = PATH + '/rboost/database/pickles/network.pkl'


  remark_types = ['standard',
                  'problem',
                  'solution',
                  'technique',
                  'reasoning',
                  'note']


  document_types = ['standard',
                    'notebook',
                    'figure'] + ['remark:' + t for t in remark_types]


  keyword_ratios = {'standard' : 0.01,
                    'notebook' : 0.1,
                    'caption'  : 0.6,
                    'remark'   : 0.6}


  date = datetime.datetime.today().strftime('%d-%m-%Y')


  def main (self):

    if not self.nested_command:
      os.system('rboost --help')
