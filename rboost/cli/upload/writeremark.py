import os
import sys

import colorama
import pandas as pd
from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.source.document.remark import Remark


@RBoost.subcommand ('write-remark')
class WriteRemark (RBoost):
  '''
  Write a special remark on RBoost database
  '''

  _ref = None
  _type = 'standard'


  @cli.switch ('--ref', str, mandatory=True)
  def ref (self, ref):
    '''
    Specify the original document
    '''

    self._ref = ref


  @cli.switch ('--type', str)
  def type (self, type):
    '''
    Specify the remark type
    '''

    if type not in self._remark_types:
      colorama.init()
      message = 'FAIL: Invalid remark type. Choose among the following types:\n\t'
      types = '\n\t'.join(self._remark_types)
      print('>>> \033[91m' + message + '\033[0m' + types)
      sys.exit()

    self._type = type


  def main (self):

    topic = input('>>> Remark topic : ')
    date = input('>>> Date (dd-mm-yyyy) : ')
    author = input('>>> Author (name-surname) : ')

    remark = Remark(date=date, author=author, topic=topic, special=self._type, reference=self._ref)
    self.create_file(remark)
    remark.open_editor()

    self.upload_file(remark)


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

      data = [[remark.date, remark.author, remark.name, remark.doctype, remark.reference]]
      new_df = pd.DataFrame(data=data, columns=db.dataframe.columns)
      db.dataframe = db.dataframe.append(new_df, ignore_index=True)

    with Network() as net:

      labs, links = remark.get_data_from_text(text)
      net.update_nodes(labs)
      net.update_edges(links)
