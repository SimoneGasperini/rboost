import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.network import Network
from rboost.source.database import Database


@RBoost.subcommand ('list-labels')
class ListLabels (RBoost):
  '''
  List the labels in RBoost database
  '''


  def main (self):

    labels = self.get_labels()
    df = self.create_dataframe(labels)

    db = Database(dataframe=df)

    db.show(full=True)


  @staticmethod
  def get_labels ():

    with Network() as net:

      labels = sorted([net.graph.nodes[n]['label'] for n in net.graph.nodes])

    return labels


  @staticmethod
  def create_dataframe (labels):

    data = [[lab.name, lab.types, lab.queries_count, lab.uploads_count]
            for lab in labels]
    df = pd.DataFrame(data=data, columns=['LABEL','TYPES','QUERIES','UPLOADS'])

    return df
