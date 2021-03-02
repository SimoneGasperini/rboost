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
    graph : networkx.Graph, default=None
      Graph which represents the RBoost's labels network
  '''

  def __init__ (self, graph=None):

    self.path = RBoost._network_pkl
    self.graph = graph


  def __enter__ (self):
    '''
    Enter the context manager reading the graph from the pickle file


    Returns
    -------
    self
    '''

    self.graph = nx.read_gpickle(self.path)

    return self


  def __exit__ (self, exc_type, exc_value, exc_traceback):
    '''
    Exit the context manager writing the graph into the pickle file
    '''

    nx.write_gpickle(self.graph, self.path)


  def get_labels (self, sort=False):
    '''
    Get the list of all the labels whitin the network


    Parameters
    ----------
    sort : bool, default=False
      If True, sort the labels by importance

    Returns
    -------
    labels : list of Label
      Labels in the network
    '''

    labels = [self.graph.nodes[node]['label'] for node in self.graph.nodes]

    if sort:
      labels.sort(reverse=True)

    return labels


  def get_kth_neighbors (self, node, k=1):
    '''
    Get all the node neighbors up to k-th order


    Parameters
    ----------
    node : str
      Source node

    k : int, default=1
      Maximum neighbors order

    Returns
    -------
    neighbors : list of str
      Neighbors up to k-th order
    '''

    nbrs = nx.single_source_shortest_path_length(G=self.graph, source=node, cutoff=k)
    neighbors = list(nbrs.keys())

    return neighbors


  def update_nodes (self, labs):
    '''
    Add new nodes to the graph or update already existing graph nodes
    according to the data contained in labs


    Parameters
    ----------
    labs : list of dict
      Labels data
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
    '''

    self.graph.clear()


  def compute_node_size (self, nodelist):
    '''
    Compute the normalized sizes of the nodes in nodelist according to their
    importance (proportional to the number of queries and uploads of the
    corresponding labels)


    Parameters
    ----------
    nodelist : list of str
      Selected nodes

    Returns
    -------
    node_size : array-like (1D)
      Array of floats representing the nodes sizes
    '''

    node_size = np.array([self.graph.nodes[n]['label'].queries_count +
                          self.graph.nodes[n]['label'].uploads_count
                          for n in nodelist])
    node_size = ((1. / np.sum(node_size)) * node_size) * 3e4

    return node_size


  def compute_node_color (self, nodelist):
    '''
    Compute the normalized colors (as floating point numbers in [0,1])
    of the nodes in nodelist according to their degree whitin the network


    Parameters
    ----------
    nodelist : list of str
      Selected nodes

    Returns
    -------
    node_color : array-like (1D)
      Array of floats representing the nodes colors
    '''

    node_color = np.array([self.graph.degree[n]
                           for n in nodelist])
    node_color = (1. / np.sum(node_color)) * node_color

    return node_color


  def show (self, nodelist=None, cmap='rainbow'):
    '''
    Show a graphical representation of the network


    Parameters
    ----------
    nodelist : list, default=graph.nodes()
      Selected nodes

    cmap : str, default='rainbow'
      Nodes color map
    '''

    if nodelist is None:
      nodelist = self.graph.nodes()

    fig, ax = plt.subplots(figsize=(10,8))

    graph = self.graph.subgraph(nodes=nodelist)
    pos = nx.drawing.layout.kamada_kawai_layout(graph)
    node_size = self.compute_node_size(nodelist)
    node_color = self.compute_node_color(nodelist)
    bbox = {'boxstyle':'round', 'ec':'black', 'fc':'white', 'alpha':0.4}

    params = {'G'           : graph,
              'pos'         : pos,
              'ax'          : ax,
              'nodelist'    : nodelist,
              'node_size'   : node_size,
              'node_color'  : node_color,
              'width'       : 0.2,
              'cmap'        : cmap,
              'bbox'        : bbox,
              'font_size'   : 10,
              }

    nx.draw_networkx(**params)

    fig.tight_layout()
    plt.axis('off')
    plt.show()



if __name__== '__main__':

  with Network() as net:
    net.show()
