import os

from tqdm import tqdm

from rboost.cli.rboost import RBoost
from rboost.source.document.pdf import PDF


@RBoost.subcommand('upload-pdfs')
class UploadPdfs (RBoost):
    """
    Upload the pdf documents to RBoost database
    """

    def main(self):

        user = self.get_user()
        date = self.get_date(auto=True)

        self.create_dirs()
        pdfs = self.get_pdfs(date, user)

        self.upload_documents(pdfs)

        self.database.push()
        self.network.push()

    def create_dirs(self):

        for item in os.listdir(self.pdfs_path):

            item_path = self.pdfs_path + item

            if os.path.isfile(item_path) and item.endswith('.pdf'):

                filename = item.replace(' ', '_')
                dirname = filename.split('.')[0]

                os.makedirs(self.pdfs_path + dirname, exist_ok=True)
                new_path = self.pdfs_path + dirname + '/' + filename
                os.rename(item_path, new_path)

    def get_pdfs(self, date, user):

        pdfs = [PDF(date=date,
                    user=user,
                    path=self.pdfs_path + dirname + '/',
                    name=dirname + '.pdf')
                for dirname in os.listdir(self.pdfs_path)
                if dirname + '.pdf' not in self.docnames]

        return pdfs

    def upload_documents(self, pdfs):

        for pdf in tqdm(pdfs, desc='Uploading documents', ncols=100):

            if pdf.text is None:
                continue

            self.upload_file(pdf)
            self.update_database(pdf)
            self.update_network(pdf)

    def upload_file(self, pdf):

        dirname = pdf.name.split('.')[0]
        filepath = pdf.path + pdf.name

        self.gdrive.create_folder(foldername=dirname, parent_folder='pdfs')
        self.gdrive.upload_file(filepath=filepath, parent_folder=dirname)

    def update_network(self, pdf):

        new_labs, new_links = pdf.get_data_from_text()
        self.network.update_nodes(new_labs)
        self.network.update_edges(new_links)

    def update_database(self, pdf):

        data = [[pdf.date, pdf.user, pdf.docname,
                 pdf.doctype, list(pdf.keywords.keys())]]
        self.database.append_data(data)
