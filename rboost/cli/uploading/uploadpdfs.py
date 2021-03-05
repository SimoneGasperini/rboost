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

    pdfs = self.get_pdfs()
    self.uploading(pdfs)


  @staticmethod
  def get_pdfs ():

    with Database() as db:

      docnames = [name for name in os.listdir(RBoost._pdfs_path)
                   if name not in list(db.dataframe['DOCNAME'])]

    pdfs = [PDF(name=name) for name in docnames]

    return pdfs


  @staticmethod
  def uploading (pdfs):

    docs_data = []

    with Network() as net:

      for pdf in pdfs:

        print(f'>>> Uploading "{pdf.name}"')
        text = pdf.get_text()
        if text is None: continue

        RBoost.gdrive.upload_file(pdf.path + pdf.name, foldername='pdfs')
        docs_data.append([pdf.docname, pdf.doctype, pdf.reference])

        new_labs, new_links = pdf.get_data_from_text(text)
        net.update_nodes(new_labs)
        net.update_edges(new_links)

    with Database() as db:

      new_df = pd.DataFrame(data=docs_data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)
