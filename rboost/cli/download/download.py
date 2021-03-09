from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.utils.autocomplete import RBAutoComplete
from rboost.utils.exception import RBException


@RBoost.subcommand ('download')
class Download (RBoost):
  '''
  Download a file/folder from RBoost database
  '''


  def main (self):

    filename = self.get_filename()

    RBoost.gdrive.download_file(filename=filename, parents='pdfs')
    print('>>> Successfully downloaded to "RBoost_Data/My_Downloads"')


  @staticmethod
  def get_filename ():

    with Database() as db:
      docnames = db.dataframe['DOCNAME'].tolist()

    RBAutoComplete(options=docnames)
    filename = input('>>> Filename (press TAB to autocomplete) :\n>>> ')

    if filename not in docnames:
      RBException(state='failure', message=f'The file "{filename}" does not exist in RBoost database')

    return filename
