from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import RBAutoComplete
from rboost.utils.exception import RBException


@RBoost.subcommand ('download')
class Download (RBoost):
  '''
  Download a document from RBoost database
  '''


  def main (self):

    docname = self.get_docname()
    RBoost.gdrive.download_folder(foldername=docname)

    print('>>> Successfully downloaded to "RBoost_Data/My_Downloads"')


  @staticmethod
  def get_docname ():

    pdfs = RBoost.gdrive.list_folder(foldername='pdfs', field='title')
    notebooks = RBoost.gdrive.list_folder(foldername='notebooks', field='title')
    docnames = pdfs + notebooks

    RBAutoComplete(options=docnames)
    name = input('\n>>> Document name (press TAB to autocomplete) :\n>>> ')

    if name not in docnames:
      RBException(state='failure', message=f'The document "{name}" does not exist in RBoost database')

    return name
