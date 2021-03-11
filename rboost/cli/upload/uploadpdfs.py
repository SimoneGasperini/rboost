import os
import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.pdf import PDF


@RBoost.subcommand ('upload-pdfs')
class UploadPdfs (RBoost):
  '''
  Upload the pdf documents on RBoost database
  '''


  def main (self):

    user = input('>>> User (name-surname) : ')

    self.create_dirs()
    pdfs = self.get_pdfs(user)
    data = []

    with Network() as net:

      for pdf in pdfs:

        print(f'>>> Uploading "{pdf.name}"')
        text = pdf.get_text()
        if text is None: continue

        self.upload_drive(pdf)
        self.update_network(net, pdf, text)

        data.append([pdf.date, pdf.user, pdf.docname, pdf.doctype])

    self.update_database(data=data)


  @staticmethod
  def get_pdfs (user):

    with Database() as db:

      already_uploaded = db.dataframe['DOCNAME'].tolist()

    for dirname in os.listdir(RBoost._pdfs_path):

      pdfs = [PDF(date = RBoost._date,
                  user = user,
                  path = RBoost._pdfs_path + dirname + '/',
                  name = dirname + '.pdf')
              for dirname in os.listdir(RBoost._pdfs_path)
              if dirname + '.pdf' not in already_uploaded]

    return pdfs


  @staticmethod
  def create_dirs ():

    for item in os.listdir(RBoost._pdfs_path):

      item_path = RBoost._pdfs_path + item

      if os.path.isfile(item_path) and item.endswith('.pdf'):

        filename = item.replace(' ','_')
        dirname = filename.split('.')[0]

        os.makedirs(RBoost._pdfs_path + dirname, exist_ok=True)
        new_path = RBoost._pdfs_path + dirname + '/' + filename
        os.rename(item_path, new_path)


  @staticmethod
  def upload_drive (pdf):

    dirname = pdf.name.split('.')[0]
    filepath = pdf.path + pdf.name

    RBoost.gdrive.create_folder(foldername=dirname, parent_folder='pdfs')
    RBoost.gdrive.upload_file(filepath=filepath, parent_folder=dirname)


  @staticmethod
  def update_network (net, pdf, text):

    new_labs, new_links = pdf.get_data_from_text(text)

    net.update_nodes(new_labs)
    net.update_edges(new_links)


  @staticmethod
  def update_database (data):

    with Database() as db:

      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)
