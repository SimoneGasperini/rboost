from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.database import Database


@RBoost.subcommand ('list-documents')
class ListDocuments (RBoost):
  '''
  List the documents in RBoost database
  '''

  _user = None
  _type = None

  @cli.switch ('--user', str)
  def user (self, user):
    '''
    Selects documents with the specified user/author
    '''

    self._user = user


  @cli.switch ('--type', str)
  def type (self, type):
    '''
    Selects documents with the specified type
    '''

    self._type = type


  def main (self):

    with Database() as db:

      if self._user is not None:
        db = db.filter_by('USER/AUTHOR', value=self._user)

      if self._type is not None:
        db = db.filter_by('DOCTYPE', value=self._type)

    db.show(full=True)
