import os
from datetime import datetime

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

  pdf_path = RBoost.PATH + '/rboost/database/pdfs/'
  pickle_path = RBoost.PATH + '/rboost/database/pickles/'


  def main (self):

    pdfs = self.get_pdfs()

    self.date = datetime.today().strftime('%d-%m-%Y')
    self.failed = []

    self.update_network(pdfs)
    self.update_database(pdfs)


  def get_pdfs (self):

    with Database(path=self.pickle_path, name='database.pkl') as db:

      filenames = [fname for fname in os.listdir(self.pdf_path)
                   if fname not in list(db.df['FILENAME'])]

    pdfs = [PDF(path=self.pdf_path, name=name) for name in filenames]

    return pdfs


  def update_network (self, pdfs):

    with Network(path=self.pickle_path, name='network.pkl') as net:

      for pdf in pdfs:

        print(f'Uploading "{pdf.name}"')
        data = pdf.get_data()

        if data is not None:
          labsinfo, relations = data
          net.update_nodes(labsinfo)
          net.update_edges(relations)

        else:
          self.failed.append(pdf.name)


  def update_database (self, pdfs):

    with Database(path=self.pickle_path, name='database.pkl') as db:

      data = [[pdf.name, pdf.filetype, self.date] for pdf in pdfs
              if pdf.name not in self.failed]

      new_df = pd.DataFrame(data=data, columns=db.df.columns)

      db.df = db.df.append(new_df, ignore_index=True)
