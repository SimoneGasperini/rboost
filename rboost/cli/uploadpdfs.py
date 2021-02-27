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

  _failed = []


  def main (self):

    pdfs = self.get_pdfs()

    self.update_network(pdfs)
    self.update_database(pdfs)


  @staticmethod
  def get_pdfs ():

    with Database() as db:

      filenames = [fname for fname in os.listdir(RBoost._pdfs_path)
                   if fname not in list(db.df['FILENAME'])]

    pdfs = [PDF(name=name) for name in filenames]

    return pdfs


  @staticmethod
  def update_network (pdfs):

    with Network() as net:

      for pdf in pdfs:

        print(f'>>> Uploading "{pdf.name}"')
        text = pdf.get_text()

        if text is None:
          UploadPdfs._failed.append(pdf.name)
          continue

        new_labs, new_links = pdf.get_data_from_text(text)
        net.update_nodes(new_labs)
        net.update_edges(new_links)


  @staticmethod
  def update_database (pdfs):

    with Database() as db:

      data = [[RBoost._date, pdf.filename, pdf.filetype, pdf.reference] for pdf in pdfs
              if pdf.name not in UploadPdfs._failed]

      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)
