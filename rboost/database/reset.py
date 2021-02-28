import os

import pandas as pd
import networkx as nx

from rboost.cli.rboost import RBoost
pickles_path = RBoost._pickles_path


# delete all the files in the pickle directory
for file in os.listdir(pickles_path):
  os.remove(pickles_path + file)


# create and init a new pickle for the files database
name = pickles_path + 'database.pkl'
open(name, 'a').close()
df = pd.DataFrame(columns=['DATE','DOCNAME','DOCTYPE','REFERENCE'])
df.to_pickle(name)


# create and init a new pickle for the labels network
name = pickles_path + 'network.pkl'
open(name, 'a').close()
graph = nx.Graph()
nx.write_gpickle(graph, name)
