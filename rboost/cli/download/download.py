import readline

from rboost.cli.rboost import RBoost
from rboost.source.database import Database


@RBoost.subcommand ('download')
class Download (RBoost):
  '''
  Download a file or a folder from RBoost database
  '''


  def main (self):

    filename = self.get_filename()
    RBoost.gdrive.download_file(filename=filename)


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

      filename = input('\n>>> Enter the filename (press TAB to autocomplete):\n>>> ')

    return filename
