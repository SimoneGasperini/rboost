import sys
import readline

import colorama

from rboost.cli.rboost import RBoost
from rboost.source.database import Database


@RBoost.subcommand ('download')
class Download (RBoost):
  '''
  Download a file/folder from RBoost database
  '''


  def main (self):

    with Database() as db:
      DOCNAMES = db.dataframe['DOCNAME'].tolist()

    filename = self.get_filename(DOCNAMES)
    self.check_filename(filename, DOCNAMES)

    RBoost.gdrive.download_file(filename=filename)
    print('>>> The file has been successfully downloaded in the folder "My_Downloads"')


  @staticmethod
  def get_filename (DOCNAMES):

    def complete (text, state):
      for name in DOCNAMES:
        if name.startswith(text):
          if state == 0:
            return name
          else:
            state -= 1

    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete)

    filename = input('\n>>> Enter the filename (press TAB to autocomplete, enter "q" to quit):\n>>> ')
    if filename == 'q': sys.exit()

    return filename


  @staticmethod
  def check_filename (filename, DOCNAMES):

    if filename not in DOCNAMES:
      colorama.init()
      message = f'FAIL: The file "{filename}" does not exist in RBoost database'
      print('>>> \033[91m' + message + '\033[0m')
      sys.exit()
