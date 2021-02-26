import os
from datetime import datetime

import colorama
import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.pdf import PDF


@RBoost.subcommand ('upload-pdfs')
class UploadPdfs (RBoost):
  '''
  Upload the pdf files on RBoost database
  '''

  date = datetime.today().strftime('%d-%m-%Y')
  failed = []


  def main (self):

    pdfs = self.get_pdfs()

    self.update_network(pdfs)
    self.update_database(pdfs)


  def get_pdfs (self):

    with Database(path=self.pkl_path, name='database.pkl') as db:

      filenames = [fname for fname in os.listdir(self.pdf_path)
                   if fname not in list(db.df['FILENAME'])]

    pdfs = [PDF(abspath=self.pdf_path, name=name) for name in filenames]

    return pdfs


  def update_network (self, pdfs):

    with Network(path=self.pkl_path, name='network.pkl') as net:

      for pdf in pdfs:

        print(f'>>> Uploading "{pdf.name}"')

        try:
          text = pdf.get_text()

        except UnicodeDecodeError:
          colorama.init()
          message = f'WARNING: The file "{pdf.name}" cannot be read'
          print('>>> \033[93m' + message + '\033[0m')
          self.failed.append(pdf.name)
          continue

        new_labs, new_links = pdf.get_data_from_text(text)
        net.update_nodes(new_labs)
        net.update_edges(new_links)


  def update_database (self, pdfs):

    with Database(path=self.pkl_path, name='database.pkl') as db:

      data = [[self.date, pdf.filename, pdf.filetype, pdf.reference] for pdf in pdfs
              if pdf.name not in self.failed]

      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)
