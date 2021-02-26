from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.database import Database


@RBoost.subcommand ('list-files')
class ListFiles (RBoost):
  '''
  List the files on RBoost database
  '''

  _filetype = None
  _date = None


  @cli.switch('--filetype', str)
  def filetype (self, filetype):
    '''
    Selects files with the specified filetype
    '''

    self._filetype = filetype


  @cli.switch('--date', str)
  def date (self, date):
    '''
    Selects files with the specified date
    '''

    self._date = date


  def main (self):

    with Database(path=self.pkl_path, name='database.pkl') as db:

      if self._filetype is not None:
        db = db.filter_by('FILETYPE', value=self._filetype)

      if self._date is not None:
        db = db.filter_by('DATE', value=self._date)

    db.show(full=True)
