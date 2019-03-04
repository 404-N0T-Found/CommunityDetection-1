#!/usr/bin/python3.6
# coding: utf-8

import random

import networkx as nx
from tqdm import tqdm


class Community:
    def __init__(self, graph=None):
        self.graph = graph
        self.nodes = list(graph.nodes())
        self.edges = list(nx.edges(self.graph))

        # Step 1: give a unique label to each node in the network
        self.labels = {node: node for node in self.nodes}

        self.nb_label = len(set(self.labels.values()))
        self.edges_common_count = self.common_count_generator()
        self.end_propagation = False

    def common_count(self, node_1, node_2):
        """
        methode qui renvoie le nombre de voisin en commun entre deux noeud
        :param graph:           NetworkX graph.
        :param node_1:      le preimier noeud de edge.
        :param node_2:      le second noeud de edge.
        """
        return int(len(set(nx.neighbors(self.graph, node_1)).intersection(set(nx.neighbors(self.graph, node_2)))))

    def common_count_generator(self):
        """

        :return: un dictionnaire pour chaque arete le nombre de voisin commun entre deux noeud
        """

        return {edge: self.common_count(edge[0], edge[1]) for edge in tqdm(self.edges)}

    def get_edges_common_count(self, neighbor, node_root):
        return self.edges_common_count[(neighbor, node_root)] \
            if (neighbor, node_root) in self.edges_common_count.keys() \
            else self.edges_common_count[(node_root, neighbor)]

    def set_labels(self, node_root, neighbors):
        scores = {}

        scores = {neighbor: (self.get_edges_common_count(neighbor, node_root) if not neighbor in scores.keys()
                             else (scores[neighbor] + self.get_edges_common_count(neighbor, node_root))) for neighbor in
                  tqdm(neighbors)}
        # TODO problem avec cette ligne (ligne 68)
        # alors si label == 1 alors on doit pas ce prendre en compte mais devenir qulqu'un d'autre
        # scores[node_root] = scores[node_root]+1 if node_root in scores.keys() else 1

        # la liste de labels max
        max_label = [self.labels[k] for k, v in scores.items() if v == max(scores.values())]

        self.labels[node_root] = int(random.sample(max_label, 1)[0])
        del scores, max_label
