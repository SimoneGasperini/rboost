import os

import pandas as pd
import networkx as nx


# delete all the files in the pickle directory
for file in os.listdir('./pickles/'):
  os.remove('./pickles/' + file)


# create and init a new pickle for the files database
name = './pickles/database.pkl'
open(name, 'a').close()
df = pd.DataFrame(columns=['FILENAME','FILETYPE','DATE'])
df.to_pickle(name)


# create and init a new pickle for the labels network
name = './pickles/network.pkl'
open(name, 'a').close()
graph = nx.Graph()
nx.write_gpickle(graph, name)
