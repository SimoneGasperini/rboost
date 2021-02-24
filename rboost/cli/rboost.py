from plumbum import cli

from rboost.cli.__path import PATH


class RBoost (cli.Application):

  PROGNAME = 'rboost'
  VERSION = '0.0.1'

  PATH = PATH


  def main (self):

    if not self.nested_command:
      print('No command given. Type "rboost --help" for help')
