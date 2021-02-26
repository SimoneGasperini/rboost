import pandas as pd


class Database ():


  def __init__ (self, path=None, name=None, df=None):

    self.path = path
    self.name = name

    self.df = df


  def __enter__ (self):

    self.df = pd.read_pickle(self.path + self.name)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):

    self.df.to_pickle(self.path + self.name)


  def filter_by (self, column, value):

    df = self.df.loc[self.df[column] == value]
    database = Database(df=df)

    return database


  def clear (self):

    self.df = self.df.iloc[0:0]


  def show (self, full=False):

    pd.set_option('colheader_justify', 'right')

    if full:
      pd.set_option('display.max_rows', None)

    print(self.df)
