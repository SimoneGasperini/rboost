import pandas as pd

from rboost.cli.rboost import RBoost
from rboost.source.network import Network
from rboost.source.database import Database


@RBoost.subcommand ('list-labels')
class ListLabels (RBoost):
  '''
  List the labels on RBoost database
  '''

  pickle_path = RBoost.PATH + '/rboost/database/pickles/'


  def main (self):

    with Network(path=self.pickle_path, name='network.pkl') as net:

      data = [[net.graph.nodes[n]['label'].name, net.graph.nodes[n]['label'].types]
              for n in net.graph.nodes]

    df = pd.DataFrame(data=data, columns=['LABEL','TYPES'])

    Database(df=df).show(tab=True)
