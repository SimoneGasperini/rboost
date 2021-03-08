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

    filename = self.get_filename()

    RBoost.gdrive.download_file(filename=filename)
    print('>>> The file has been successfully downloaded in the folder "My_Downloads"')


  @staticmethod
  def get_filename ():

    with Database() as db:
      DOCNAMES = db.dataframe['DOCNAME'].tolist()    

    def complete (text, state):
      for name in DOCNAMES:
        if name.startswith(text):
          if state == 0:
            return name
          else:
            state -= 1

    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete)

    filename = input('>>> Filename (press TAB to autocomplete)\n>>> ')

    if filename not in DOCNAMES:
      colorama.init()
      message = f'FAIL: The file "{filename}" does not exist in RBoost database'
      print('>>> \033[91m' + message + '\033[0m')
      sys.exit()

    return filename
