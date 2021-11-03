from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand('download')
class Download (RBoost):
    """
    Download a document from RBoost database
    """

    def main(self):

        docname = self.get_docname()
        self.gdrive.download_folder(foldername=docname)

        print('>>> Successfully downloaded to "RBoost_Data/My_Downloads"')

    def get_docname(self):

        pdfs = self.gdrive.list_folder(foldername='pdfs', field='title')
        notebooks = self.gdrive.list_folder(
            foldername='notebooks', field='title')
        documents = pdfs + notebooks

        with AutoComplete(options=documents):
            docname = input('>>> Document name :\n>>> ')

        if docname not in documents:
            e = Exceptions(state='failure',
                           message=f'The document "{docname}" does not exist in RBoost database')
            e.throw()

        return docname
