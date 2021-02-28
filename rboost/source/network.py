from collections import Counter

import networkx as nx
import numpy as np
import pylab as plt

from rboost.cli.rboost import RBoost
from rboost.source.label import Label


class Network ():
  '''
  Class for the RBoost's network object


  Parameters
  ----------
    path : str, default='./rboost/rboost/database/pickles/network.pkl'
      Local path to the network pickle file

    graph : networkx.Graph, default=None
      Graph which represents the RBoost's labels network
  '''

  def __init__ (self, pathname=RBoost._network_pkl, graph=None):

    self.pathname = pathname
    self.graph = graph


  def __enter__ (self):
    '''
    Enter the context manager reading the graph from the pickle file


    Returns
    -------
    self
    '''

    self.graph = nx.read_gpickle(self.pathname)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):
    '''
    Exit the context manager writing the graph into the pickle file


    Returns
    -------
    None
    '''

    nx.write_gpickle(self.graph, self.pathname)


  def update_nodes (self, labs):
    '''
    Add new nodes to the graph or update already existing graph nodes
    according to the data contained in labs


    Parameters
    ----------
    labs : list of dict
      Labels data

    Returns
    -------
    None
    '''

    new_nodes = [dic['name'] for dic in labs
                 if dic['name'] not in self.graph.nodes]

    for node in new_nodes:
      self.graph.add_node(node, label=Label(name=node))

    for dic in labs:
      node = dic['name']
      self.graph.nodes[node]['label'].update(dic)


  def update_edges (self, links):
    '''
    Add new edges to the graph or update already existing graph edges
    according to the data contained in links


    Parameters
    ----------
    links : list of tuple
      Links between labels

    Returns
    -------
    None
    '''

    new_edges = [link for link in links
                 if link not in self.graph.edges]

    for (node1, node2) in new_edges:
      self.graph.add_edge(node1, node2, edge_count=0)

    edges_counter = Counter(links)

    for edge in edges_counter:
      node1, node2 = edge
      self.graph[node1][node2]['edge_count'] += edges_counter[edge]


  def clear (self):
    '''
    Clear the network by removing all the graph nodes and edges


    Returns
    -------
    None
    '''

    self.graph.clear()


  def compute_node_size (self):
    '''
    Compute the normalized sizes of the graph nodes according to their
    importance whitin the network (directly proportional to uses number of the
    label)


    Returns
    -------
    node_size : array-like (1D) of float
      Nodes sizes

    Notes
    -----
    .. note::
      This has only visualization purposes
    '''

    node_size = np.array([self.graph.nodes[n]['label'].queries_count +
                          self.graph.nodes[n]['label'].uploads_count
                          for n in self.graph.nodes])
    node_size = ((1. / np.sum(node_size)) * node_size) * 4e4

    return node_size


  def compute_node_color (self):
    '''
    Compute the normalized colors (as floating point numbers in [0,1])
    of the graph nodes according to their degree (links number of the label)


    Returns
    -------
    node_color : array-like (1D) of float
      Numbers representing the nodes colors

    Notes
    -----
    .. note::
      This has only visualization purposes
    '''

    node_color = np.array([self.graph.degree[n]
                           for n in self.graph.nodes])
    node_color = (1. / np.sum(node_color)) * node_color

    return node_color


  def show (self, cmap='rainbow'):
    '''
    Show a graphical representation of the labels network


    Parameters
    ----------
    cmap : str, default='rainbow'
      Nodes color map

    Returns
    -------
    None
    '''

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
