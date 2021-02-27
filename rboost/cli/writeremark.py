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


  def main (self, name):

    dirpath = self._remarks_path + self._ref + '/'
    os.makedirs(dirpath, exist_ok=True)

    name = self._date + '_' + name + '.txt'
    remark = Remark(path=dirpath, name=name, special=self._type, reference=self._ref)
    self.check_file (remark)

    remark.open_editor()

    self.upload_file(remark)


  @staticmethod
  def check_file (remark):

    with Database() as db:

      if remark.filename in list(db.df['FILENAME']):
        raise NotImplementedError('Not implemented yet!') # TODO

    if remark.name not in os.listdir(remark.path):
      open(remark.path + remark.name, mode='w').close()


  @staticmethod
  def upload_file (remark):

    print(f'>>> Are you sure to upload the file "{remark.name}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'>>> Uploading "{remark.filename}"')
    text = remark.get_text()

    with Database() as db:

      data = [[RBoost._date, remark.name, remark.filetype, remark.reference]]
      new_df = pd.DataFrame(data=data, columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)

    with Network() as net:

      labs, links = remark.get_data_from_text(text)
      net.update_nodes(labs)
      net.update_edges(links)
