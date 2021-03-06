import sys

import colorama
from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.database import Database


@RBoost.subcommand ('list-documents')
class ListDocuments (RBoost):
  '''
  List the documents in RBoost database
  '''

  _type = None


  @cli.switch ('--type', str)
  def type (self, type):
    '''
    Selects documents with the specified type
    '''

    if type not in self._document_types:
      colorama.init()
      message = 'FAIL: Invalid document type. Choose among the following types:\n\t'
      types = '\n\t'.join(self._document_types)
      print('>>> \033[91m' + message + '\033[0m' + types)
      sys.exit()

    self._type = type


  def main (self):

    with Database() as db:

      if self._type is not None:
        db = db.filter_by('DOCTYPE', value=self._type)

    db.show(full=True)
