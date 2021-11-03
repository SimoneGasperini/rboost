import os
import math
from collections import Counter

import networkx as nx
import pyvis

from rboost.source.label import Label
from rboost.source.link import Link
from rboost.utils.exceptions import Exceptions
from rboost.utils.colormapper import ColorMapper


class Network:
    """
    Class for RBoost's labels network


    Parameters
    ----------
    filepath : str
      Local path to the network pickle file

    gdrive : gdrive.GDrive
      RBoost's Google Drive object
    """

    def __init__(self, filepath, gdrive):

        self.filepath = filepath
        self.gdrive = gdrive

        self.gdrive.download_file(filename=os.path.basename(self.filepath))
        self.graph = nx.readwrite.read_gpickle(self.filepath)

        os.remove(self.filepath)

    def push(self):
        """
        Write the network pickle file and upload it to Google Drive
        """

        nx.readwrite.write_gpickle(self.graph, self.filepath)
        self.gdrive.upload_file(self.filepath)

        os.remove(self.filepath)

    def get_kth_neighbors(self, node, k=1):
        """
        Get all the neighboring nodes of a node up to k-th order


        Parameters
        ----------
        node : str
          Source node

        k : int, default=1
          Maximum neighbors order

        Returns
        -------
        neighbors : list of str
          Neighboring nodes
        """

        nbrs = nx.single_source_shortest_path_length(
            G=self.graph, source=node, cutoff=k)
        neighbors = list(nbrs.keys())

        return neighbors

    def get_nearest_nodes(self, node, distance):
        """
        Get all the nodes within a maximum distance from a node


        Parameters
        ----------
        node : str
          Source node

        distance : float
          Maximum distance

        Returns
        -------
        nearest_nodes : list of str
          Nodes within the distance
        """

        def euclid_dist(pos, n, m):
            return math.sqrt((pos[n][0] - pos[m][0])**2 + (pos[n][1] - pos[m][1])**2)

        positions = nx.drawing.layout.kamada_kawai_layout(self.graph)
        nearest_nodes = [other for other in self.graph.nodes
                         if euclid_dist(pos=positions, n=node, m=other) <= distance]

        return nearest_nodes

    def get_path(self, source, target):
        """
        Get the shortest path between two nodes


        Parameters
        ----------
        source : str
          Source node

        target : str
          Target node

        Returns
        -------
        path : list of str
          All nodes in the path
        """

        path = None

        try:
            path = nx.shortest_path(G=self.graph, source=source, target=target)

        except nx.exception.NetworkXNoPath:
            e = Exceptions(state='failure',
                           message='Such path was not found in RBoost network')
            e.throw()

        return path

    def update_nodes(self, labs):
        """
        Add new nodes to the graph or update already existing graph nodes
        according to the data contained in labs


        Parameters
        ----------
        labs : list of dict
          Labels data
        """

        new_nodes = [dic['name'] for dic in labs
                     if dic['name'] not in self.graph.nodes]

        for node in new_nodes:
            self.graph.add_node(node, label=Label(name=node))

        for dic in labs:
            node = dic['name']
            self.graph.nodes[node]['label'].update(dic)

    def update_edges(self, links):
        """
        Add new edges to the graph or update already existing graph edges
        according to the data contained in links


        Parameters
        ----------
        links : list of tuple
          Links between labels
        """

        new_edges = [link for link in links
                     if link not in self.graph.edges]

        for (node1, node2) in new_edges:
            self.graph.add_edge(node1, node2, edge_count=0)

        edges_counter = Counter(links)

        for edge in edges_counter:
            node1, node2 = edge
            self.graph[node1][node2]['edge_count'] += edges_counter[edge]

    def compute_nodes_size(self, nodelist, scale):
        """
        Compute the scaled size of each node in nodelist according to their
        importance (proportional to the number of queries and uploads of the
        corresponding label)


        Parameters
        ----------
        nodelist : list of str
          Selected nodes

        scale : float
          Nodes size scaling factor

        Returns
        -------
        nodes_size : list of float
          Numbers representing the nodes size
        """

        counts = [self.graph.nodes[n]['label'].queries_count + self.graph.nodes[n]['label'].uploads_count
                  for n in nodelist]
        norm = 1. / max(counts)
        nodes_size = [count*norm*scale for count in counts]

        return nodes_size

    def compute_nodes_color(self, nodelist, cmap):
        """
        Compute the normalized color (in html hexadecimal format) of each
        node in nodelist according to their degree within the network


        Parameters
        ----------
        nodelist : list of str
          Selected nodes

        cmap : str, default='rainbow'
          Nodes color map

        Returns
        -------
        nodes_color : list of str
          Colors in html hexadecimal format
        """

        degrees = [self.graph.degree[n] for n in nodelist]
        norm = 1. / max(degrees)

        cmapper = ColorMapper(cmap_name=cmap)
        nodes_color = [cmapper.float2hex(deg*norm) for deg in degrees]

        return nodes_color

    def show(self, filepath, nodelist=None, scale=15., cmap='rainbow'):
        """
        Show an interactive graphical representation of the network containing
        the selected nodes and save the output in the specified file


        Parameters
        ----------
        filepath : str
          Path and name of the output html file

        nodelist : list of str, default=None
          Selected nodes

        scale : float, default=800.
          Nodes size scaling factor

        cmap : str, default='rainbow'
          Nodes color map
        """

        if nodelist is None:
            nodelist = self.graph.nodes()
        graph = self.graph.subgraph(nodes=nodelist)

        pos = nx.drawing.layout.kamada_kawai_layout(graph)
        nodes_size = self.compute_nodes_size(nodelist, scale=scale)
        nodes_color = self.compute_nodes_color(nodelist, cmap=cmap)

        net = pyvis.network.Network(height='100%', width='100%')

        labels = {}
        node_ids = {}
        for n_id, node, size, color in zip(range(len(nodelist)), nodelist, nodes_size, nodes_color):
            label = graph.nodes[node].pop('label')
            net.add_node(n_id=n_id, label=node, x=pos[node][0]*500, y=pos[node][1]*500,
                         title=label.to_html(), size=size, color=color)
            labels[node] = label
            node_ids[node] = n_id

        for node1, node2 in graph.edges():
            link = Link(node1=node1, node2=node2, labels=labels)
            net.add_edge(source=node_ids[node1], to=node_ids[node2],
                         title=link.to_html(), width=0.001, color='black')

        net.toggle_physics(False)
        net.show(name=filepath)
