import os

import pandas as pd

from rboost.cli.rboost import RBoost


class Database ():
  '''
  Class for the RBoost's database object


  Parameters
  ----------
    dataframe : pandas.DataFrame, default=None
      Table which represents the RBoost's documents database
  '''

  def __init__ (self, dataframe=None):

    self.filepath = RBoost._database_pkl
    self.filename = os.path.basename(self.filepath)

    self.dataframe = dataframe


  def __enter__ (self):
    '''
    Enter the context manager downloading the Google Drive database pickle file
    and reading its content


    Returns
    -------
    self
    '''

    RBoost.gdrive.download_file(self.filename)
    self.dataframe = pd.read_pickle(self.filepath)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):
    '''
    Exit the context manager uploading the database pickle file to Google Drive
    '''

    self.dataframe.to_pickle(self.filepath)
    RBoost.gdrive.update_file(self.filepath)

    os.remove(self.filepath)


  def filter_by (self, column, value):
    '''
    Filter the database selecting only the table rows whose entry in the
    given column is equal to the given value


    Parameters
    ----------
    column : str
      Column name

    value : str
      Value to check in the given column

    Returns
    -------
    database : Database
      Filtered database
    '''

    dataframe = self.dataframe.loc[self.dataframe[column] == value]
    database = Database(dataframe=dataframe)

    return database


  def clear (self):
    '''
    Clear the database by removing all the table rows
    '''

    self.dataframe = self.dataframe.iloc[0:0]


  def show (self, full=False):
    '''
    Print the database table to terminal


    Parameters
    ----------
    full : bool, default=False
      If True, display all the rows
    '''

    pd.set_option('colheader_justify', 'right')

    if full:
      pd.set_option('display.max_rows', None)

    print(self.dataframe)
