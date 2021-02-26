import os
import sys
from datetime import datetime

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


  @cli.switch('--type', str, mandatory=True)
  def type (self, type):
    '''
    Specify the remark type
    '''

    self._type = type

  date = datetime.today().strftime('%d-%m-%Y')


  def main (self, reference):

    dirname = reference.replace('/','_')
    os.makedirs(self.r_path + dirname, exist_ok=True)

    remark = Remark(abspath=self.r_path, dirname=dirname,
                    special=self._type, date=self.date, reference=reference)

    self.open_editor(remark)
    self.upload_file(remark)


  def open_editor (self, remark):

    if sys.platform.startswith('win'):
      os.system('notepad ' + remark.path + remark.name)

    elif sys.platform.startswith('linux'):
      os.system('gedit ' + remark.path + remark.name)

    else:
      raise SystemError


  def upload_file (self, remark):

    print(f'>>> Are you sure to upload the file "{remark.name}" on RBoost database?')
    if not input('>>> (y/n) ') == 'y': sys.exit()

    print(f'>>> Uploading "{remark.filename}"')

    text = remark.get_text()

    with Database(path=self.pkl_path, name='database.pkl') as db:

      new_df = pd.DataFrame(data=[[self.date, remark.name, remark.filetype, remark.reference]],
                            columns=db.df.columns)
      db.df = db.df.append(new_df, ignore_index=True)

    with Network(path=self.pkl_path, name='network.pkl') as net:

      labs, links = remark.get_data_from_text(text)
      net.update_nodes(labs)
      net.update_edges(links)
