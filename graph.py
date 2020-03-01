# -*- encoding: utf-8 -*-
"""
A program that implements dijkstras algorithm for shortest path.

:author: Andre Filliettaz
:email: andrentaz@gmail.com
:github: https://github.com/andrentaz
"""
from __future__ import absolute_import, unicode_literals

from enum import Enum

from helpers import BinaryMinHeap, Queue


class Edge(object):
    """Implements an abstractio to graph's Edge"""
    def __init__(self, source, neighboor, distance):
        super(Edge).__init__()
        self.source = source
        self.neighboor = neighboor
        self.distance = distance

    def __repr__(self):
        return (
            'Edge(source={} '
            'neighboor={}, '
            'distance={})'
        ).format(
            self.source.label,
            self.neighboor.label,
            self.distance,
        )


class Vertex(object):
    """Implements an abstraction to graph's Vertex"""
    class Color(Enum):
        """For First-Search purpuses"""
        WHITE = 0
        GREY = 1
        BLACK = 2

    def __init__(self, label, distance=float("inf")):
        super(Vertex).__init__()
        self.label = label
        self.distance = distance
        self.edges = []
        self.previous = None
        self.visited = False
        self.color = Vertex.Color.WHITE

    def __repr__(self):
        return (
            'Vertex(label={}, '
            'distance={}, '
            'edges={}, '
            'previous={}, '
            'visited={}, '
            'color={})'
        ).format(
            self.label,
            self.distance,
            len(self.edges),
            self.previous.label if self.previous else None,
            self.visited,
            self.color,
        )

    def add_edge(self, vertex, dist):
        """Add edges to the Vertex"""
        self.edges.append(Edge(self, vertex, dist))

    @property
    def neighboors(self):
        """Give a list of Vertex neighboors"""
        return [
            e.neighboor
            for e in self.edges
        ]

    def __gt__(self, other):
        """Overload the greater than operator"""
        return self.distance > other.distance


class Graph(object):
    """Implements an abstraction to Graphs using a list of vertexes"""
    def __init__(self):
        super(Graph).__init__()
        self.vertexes = []

    def __repr__(self):
        return ('Graph(vertexes={})').format(len(self.vertexes))

    def create_from_file(self, filename, digraph=False):
        """Create a graph from a file with a matrix of distances"""

        # read matrix of distances from file
        with open(filename, 'r') as adjacency_list:
            for row_idx, row in enumerate(adjacency_list):
                # the first row contains the number of vertexes
                if row_idx == 0:
                    number_of_vertexes = int(row)

                    # initialize the vertex list
                    for i in range(number_of_vertexes):
                        self.vertexes.append(Vertex(str(i)))

                    continue

                # from the second row in the lines are structured as:
                # 'from to weight'
                line = row.split(' ')
                from_idx = int(line[0])
                to_idx = int(line[1])
                weight = int(line[2])

                v_from = self.vertexes[from_idx]
                v_to = self.vertexes[to_idx]

                v_from.add_edge(v_to, weight)

                if not digraph:
                    v_to.add_edge(v_from, weight)

    def reset(self):
        """Reset the graph to run dijkstra from other start nodes"""
        for vertex in self.vertexes:
            vertex.previous = None
            vertex.distance = float('inf')
            vertex.visited = False
            vertex.color = Vertex.Color.WHITE

    def dijkstra(self, start, end=None):
        """
        Run the dijkstra algorithm to find the shortest path from start node to
        end node using a BinaryMinHeap to keep the priority queue efficient.

        If no end node is passed, this algorithm will find the min distance of
        every node from the start.

        :param start: starting node
        :param end: end node
        """

        # setup vertex heap based in distance
        start.distance = 0
        vertex_heap = BinaryMinHeap(self.vertexes)
        vertex_heap.build_min_heap()

        # run the loop checking for edges
        while vertex_heap.heap:
            # get the next in the priority queue
            node = vertex_heap.extract_min()

            # loop over the node edges
            for edge in node.edges:
                neighboor = edge.neighboor
                if neighboor.visited:
                    continue

                path_distance = node.distance + edge.distance

                if path_distance < neighboor.distance:
                    neighboor.distance = path_distance
                    neighboor.previous = node

            # check if the end node is the one popped and the algorithm can end
            node.visited = True
            if end and node == end:
                break

    def path(self, start, end, run_dijkstra=False):
        """
        Get the shortest path from start to end after the dijkstra algorithm is
        runned in the graph.

        :param start: starting node
        :param end: end node
        :param run_dijkstra: if true will run a complete dijkstra in the graph
        previously to defining the shortest path between start and end.

        :return path: dict with path from start to end and total distance
        """
        path = []

        if not start.distance == 0:
            if not run_dijkstra:
                return None
            self.dijkstra(start)

        # case we have a disconnected graph
        if end.distance == float('inf'):
            return {
                'distance': end.distance,
                'path': path,
            }

        # get the reversed path
        node = end
        while node != start:
            path.append(node)
            node = node.previous

        path.append(start)

        return {
            'distance': end.distance,
            'path': list(reversed(path)),
        }

    def breadth_first_search(self, start):
        """
        Run a Breadth First Search algorithm in the given graph begining in the
        start node.

        :param start: Vertex from which the search starts
        :return search_tree: list of Edges from the search tree
        """
        start.color = Vertex.Color.GREY
        search_tree = []
        grey_nodes = Queue([start])

        while len(grey_nodes) > 0:
            node = grey_nodes.pop()

            for edge in node.edges:
                neighboor = edge.neighboor
                # add edge to search tree and color the node
                if neighboor.color == Vertex.Color.WHITE:
                    search_tree.append(edge)
                    neighboor.color = Vertex.Color.GREY
                    grey_nodes.add(neighboor)


            # paint the node black
            node.color = Vertex.Color.BLACK

        return search_tree

    def depth_first_search(self, start, search_tree=[]):
        """
        Run a Depth First Search algorithm in the given graph begining in the
        start node.

        :param start: Vertex from which the search starts
        :return search_tree: list of Edges from the search tree
        """
        start.color = Vertex.Color.GREY

        for edge in start.edges:
            neighboor = edge.neighboor

            if neighboor.color == Vertex.Color.WHITE:
                search_tree.append(edge)
                self.depth_first_search(
                    start=neighboor,
                    search_tree=search_tree,
                )

        start.color = Vertex.Color.BLACK
        return search_tree
