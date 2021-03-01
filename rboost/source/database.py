import pandas as pd

from rboost.cli.rboost import RBoost


class Database ():
  '''
  Class for the RBoost's database object


  Parameters
  ----------
    path : str, default='<database_path>'
      Local path to the database pickle file

    df : pandas.DataFrame, default=None
      Table which represents the RBoost's documents database
  '''

  def __init__ (self, path=RBoost._database_pkl, df=None):

    self.path = path
    self.df = df


  def __enter__ (self):
    '''
    Enter the context manager reading the table from the pickle file


    Returns
    -------
    self
    '''

    self.df = pd.read_pickle(self.path)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):
    '''
    Exit the context manager writing the table into the pickle file


    Returns
    -------
    None
    '''

    self.df.to_pickle(self.path)


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

    df = self.df.loc[self.df[column] == value]
    database = Database(df=df)

    return database


  def clear (self):
    '''
    Clear the database by removing all the table rows


    Returns
    -------
    None
    '''

    self.df = self.df.iloc[0:0]


  def show (self, full=False):
    '''
    Print the database table to terminal


    Parameters
    ----------
    full : bool, default=False
      If True, display all the rows

    Returns
    -------
    None
    '''

    pd.set_option('colheader_justify', 'right')

    if full:
      pd.set_option('display.max_rows', None)

    print(self.df)



if __name__== '__main__':

  with Database() as db:
    db.show()
