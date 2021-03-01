import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.network import Network
from rboost.source.database import Database


@RBoost.subcommand ('list-labels')
class ListLabels (RBoost):
  '''
  List the labels on RBoost database
  '''


  def main (self):

    with Network() as net:

      data = [[net.graph.nodes[n]['label'].name, net.graph.nodes[n]['label'].types]
              for n in net.graph.nodes]

    db = Database(dataframe=pd.DataFrame(data=data, columns=['LABEL','TYPES']))

    db.show(full=True)
