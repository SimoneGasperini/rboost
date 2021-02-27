from collections import Counter

import networkx as nx
import numpy as np
import pylab as plt

from rboost.source.label import Label
from rboost.cli.rboost import RBoost
NET_PATH = RBoost.network_pkl


class Network ():


  def __init__ (self, pathname=NET_PATH, graph=None):

    self.pathname = pathname
    self.graph = graph


  def __enter__ (self):

    self.graph = nx.read_gpickle(self.pathname)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):

    nx.write_gpickle(self.graph, self.pathname)


  def add_new_nodes (self, labs):

    new_nodes = [dic['name'] for dic in labs
                 if dic['name'] not in self.graph.nodes]

    for node in new_nodes:
      self.graph.add_node(node, label=Label(name=node))


  def update_nodes (self, labs):

    self.add_new_nodes(labs)

    for dic in labs:
      node = dic['name']
      self.graph.nodes[node]['label'].update(dic)


  def add_new_edges (self, links):

    new_edges = [link for link in links
                 if link not in self.graph.edges]

    for (node1, node2) in new_edges:
      self.graph.add_edge(node1, node2, edge_count=0)


  def update_edges (self, links):

    self.add_new_edges(links)

    edges_counter = Counter(links)

    for edge in edges_counter:
      node1, node2 = edge
      self.graph[node1][node2]['edge_count'] += edges_counter[edge]


  def clear (self):

    self.graph.clear()


  def compute_node_size (self):

    node_size = np.array([self.graph.nodes[n]['label'].queries_count +
                          self.graph.nodes[n]['label'].uploads_count
                          for n in self.graph.nodes])
    node_size = ((1. / np.sum(node_size)) * node_size) * 4e4

    return node_size


  def compute_node_color (self):

    node_color = np.array([self.graph.degree[n]
                           for n in self.graph.nodes])
    node_color = (1. / np.sum(node_color)) * node_color

    return node_color


  def show (self, cmap='rainbow'):

    fig, ax = plt.subplots(figsize=(10,8))

    pos = nx.drawing.layout.kamada_kawai_layout(self.graph)
    node_size = self.compute_node_size()
    node_color = self.compute_node_color()
    bbox = {'boxstyle':'round', 'ec':'black', 'fc':'white', 'alpha':0.4}

    nx.draw_networkx(G           = self.graph,
                     pos         = pos,
                     ax          = ax,
                     node_size   = node_size,
                     node_color  = node_color,
                     width       = 0.2,
                     cmap        = cmap,
                     bbox        = bbox,
                     font_size   = 10,
                     font_weight = 'bold')

    fig.tight_layout()
    plt.axis('off')
    plt.show()



if __name__== '__main__':

  with Network() as net:
    net.show()
