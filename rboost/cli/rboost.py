from plumbum import cli

from rboost.cli.__path import PATH


class RBoost (cli.Application):

  PROGNAME = 'rboost'
  VERSION = '0.0.1'

  pdf_path = PATH + '/rboost/database/pdfs/'
  nb_path = PATH + '/rboost/database/notebooks/'
  r_path = PATH + '/rboost/database/remarks/'
  pkl_path = PATH + '/rboost/database/pickles/'


  def main (self):

    if not self.nested_command:
      print('No command given. Type "rboost --help" for help')
