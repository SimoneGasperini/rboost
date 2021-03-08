import os
import sys
import readline

import colorama
import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.remark import Remark


@RBoost.subcommand ('write-remark')
class WriteRemark (RBoost):
  '''
  Write a special remark on RBoost database
  '''


  def main (self):

    reference = self.get_ref()

    special = input('>>> Remark type : ')
    topic = input('>>> Remark topic : ')

    date = input('>>> Date (dd-mm-yyyy) : ')
    author = input('>>> Author (name-surname) : ')

    remark = Remark(date=date, user=author, topic=topic, special=special, reference=reference)
    self.create_file(remark)
    remark.open_editor()

    self.upload_file(remark)


  @staticmethod
  def get_ref ():

    with Database() as db:
      DOCNAMES = db.dataframe['DOCNAME'].tolist()    

    def complete (text, state):
      for name in DOCNAMES:
        if name.startswith(text):
          if state == 0:
            return name
          else:
            state -= 1

    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete)

    ref = input('>>> Reference file (press TAB to autocomplete)\n>>> ')

    if ref not in DOCNAMES:
      colorama.init()
      message = f'FAIL: The file "{ref}" does not exist in RBoost database'
      print('>>> \033[91m' + message + '\033[0m')
      sys.exit()

    return ref


  @staticmethod
  def create_file (remark):

    os.makedirs(remark.path, exist_ok=True)
    open(remark.path + remark.name, mode='w').close()


  @staticmethod
  def upload_file (remark):

    print(f'>>> Are you sure to upload the file "{remark.name}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'>>> Uploading "{remark.docname}"')
    text = remark.get_text()

    with Database() as db:

      data = [[remark.date, remark.user, remark.name, remark.doctype, remark.reference]]
      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)

    with Network() as net:

      labs, links = remark.get_data_from_text(text)
      net.update_nodes(labs)
      net.update_edges(links)
