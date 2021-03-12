import os
import sys
import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.remark import Remark
from rboost.utils.autocomplete import RBAutoComplete
from rboost.utils.exception import RBException


@RBoost.subcommand ('write-remark')
class WriteRemark (RBoost):
  '''
  Write a special remark on RBoost database
  '''


  def main (self):

    reference = self.get_reference()
    path = RBoost._remarks_path + reference + '/'
    os.makedirs(path, exist_ok=True)

    name = input('>>> Remark name : ')
    special = input('>>> Remark type : ')

    remark = Remark(date=None, user=None, path=path, name=name, special=special)
    self.create_file(remark)

    remark.open_editor()

    self.upload_file(remark)

    self.update_database(remark)
    self.update_network(remark)


  @staticmethod
  def get_reference ():

    with Database() as db:
      df = db.dataframe.loc[db.dataframe['DOCTYPE'].isin(['standard','notebook'])]
      docnames = list(set([docname.split('/')[0].split('.')[0]
                           for docname in df['DOCNAME']]))

    RBAutoComplete(options=docnames)
    ref = input('\n>>> Reference file (press TAB to autocomplete) :\n>>> ')

    if ref not in docnames:
      RBException(state='failure', message=f'The document "{ref}" does not exist in RBoost database')

    return ref


  @staticmethod
  def create_file (remark):

    if not os.path.exists(remark.path + remark.name):
      open(remark.path + remark.name, mode='w').close()


  @staticmethod
  def upload_file (remark):

    print(f'>>> Do you want to upload the file "{remark.docname}" on RBoost database?')
    answer = input('>>> (y/n) ')
    if not answer == 'y':
      sys.exit()

    remark.date = input('>>> Date (dd-mm-yyyy) : ')
    remark.user = input('>>> Author (name-surname) : ')

    print(f'>>> Uploading "{remark.docname}"')

    filepath = remark.path + remark.name
    folder = os.path.basename(remark.path[:-1])
    RBoost.gdrive.upload_file(filepath=filepath, parent_folder=folder)


  @staticmethod
  def update_database (remark):

    with Database() as db:

      data = [[remark.date, remark.user, remark.name, remark.doctype]]

      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)


  @staticmethod
  def update_network (remark):

    text = remark.get_text()

    with Network() as net:

      labs, links = remark.get_data_from_text(text)

      net.update_nodes(labs)
      net.update_edges(links)
