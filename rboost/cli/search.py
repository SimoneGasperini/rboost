import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand ('search')
class Search (RBoost):
  """
  Search the RBoost's documents by label
  """

  def main (self, *args):

    labels = list(args)
    self.check_labels(labels)

    self.update_labels(labels)
    self.network.push()

    df = self.filter_dataframe(labels)
    self.show_dataframe(df=df, full=False)

  def check_labels (self, labels):

    for label in labels:
      if label not in self.labnames:
        e = Exceptions(state='failure',
                       message=f'The label "{label}" was not found in RBoost network')
        e.throw()

  def update_labels (self, labels):

    for node in labels:
      self.network.graph.nodes[node]['label'].queries_count += 1

  def filter_dataframe (self, labels):

    documents = [row for index, row in self.database.dataframe.iterrows()
                 if all(label in row['KEYWORDS'] for label in labels)]

    df = pd.DataFrame(data=documents, columns=self.dataframe_columns)

    return df
