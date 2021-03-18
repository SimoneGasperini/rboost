from plumbum import cli
from rboost.cli.rboost import RBoost


@RBoost.subcommand ('list-documents')
class ListDocuments (RBoost):
  """
  List the documents in RBoost database
  """

  _user = None
  _doctype = None

  @cli.switch ('--user', str)
  def user (self, user):
    """
    Selects documents with the specified user/author
    """

    self._user = user

  @cli.switch ('--doctype', str)
  def doctype (self, doctype):
    """
    Selects documents with the specified type
    """

    self._doctype = doctype

  def main (self):

    df = self.database.dataframe

    if self._user is not None:
      df = df.loc[df['USER/AUTHOR'] == self._user]

    if self._doctype is not None:
      df = df.loc[df['DOCTYPE'] == self._doctype]

    self.show_dataframe(df=df, full=False)
