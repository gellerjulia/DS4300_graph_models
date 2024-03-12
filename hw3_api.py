"""
Ceara Zhang
DS 4300
HW 4 Graph Data Models

Created: 10 March 2024
Updated: 12 March 2024

hw4_api.py:
Graph Data API for Redis.
"""

import redis
from typing import List


class GraphDataAPI:

    def __init__(self, port: int):
        """
        Establish connection with Redis.
        """
        self.r = redis.Redis('localhost', port, decode_responses=True)

    def close(self):
        """
        Close Ronnection to Redis.
        """
        self.r.close()

    def destroy_database(self):
        """
        Destroy the database for rerunning purposes
        """
        # clear Redis Data
        self.r.flushall()

    def add_node(self, name: str, type: str):
        """
        Add a node to the database of a given name and type

        Args:
        name: str, name of node item.
        type: str, one-word categorical description of node.

        """
        # check to see if tweet_id exists: if not, set one for autoincrementation
        if self.r.exists('node_id'):
            node_id = int(self.r.get('node_id'))
        else:
            self.r.set('node_id', 0)
            node_id = int(self.r.get('node_id'))
        # create node
        self.r.set(f'node:<{name}>', node_id)
        # record node's type
        self.r.set(f'type:<{node_id}>', type)
        # note the types of nodes in a set
        self.r.sadd('node_type_list', type)
        # autoincrement
        self.r.incr('node_id')

    def get_node_type(self, node: str) -> str:
        """
        Get type of node.

        Args:
        node: str, the node to find type information of

        Returns:
        node_type: str, node's type.
        """
        node_id = int(self.r.get(f'node:<{node}>'))
        node_type = str(self.r.get(f'type:<{node_id}>'))
        return node_type

    def add_edge(self, name1: str, name2: str, type: str):
        """
        Add an edge between two nodes. Unique edge connection types are recorded.

        Args:
        name1: str, the node which the edge is drawn from.
        name2: str, the node which the edge is drawn to.
        type: str, one-word categorical description of edge.
        """
        # check if nodes exist
        if not (self.r.exists(f'node:<{name1}>') & self.r.exists(f'node:<{name2}>')):
            raise Exception('Node(s) do not exist')
        # create a set of edges leading from each node
        self.r.sadd(f'{type}:<{name1}>', name2)
        # record edge types
        self.r.sadd('edge_type_list', type)
        # record node-edge types relationship
        self.r.set(self.get_node_type(name2), type)

    def get_adjacent(self, name: str, node_type=None, edge_type=None) -> List[str]:
        """
        Get the names of all adjacent nodes. User may optionally specify that the adjacent nodes are
        of a given type and/or only consider edges of a given type.

        Args:
        name: str, the desired node to find adjacent connections to.
        node_type: default none, str, the desired type of adjacent node.
        edge_type: default none, str, the desired type of edge connection.

        Returns:
        adjacent_nodes: List[str], list of adjacent nodes.
        """
        # get adjacent nodes if type fields are empty
        if (node_type is None) & (edge_type is None):
            adjacent_nodes = set([])
            # get all edge types and the associated connections
            for i in list(self.r.smembers('edge_type_list')):
                adjacent_nodes = adjacent_nodes.union(set(self.r.smembers(f'{i}:<{name}>')))
            adjacent_nodes = list(adjacent_nodes)
        # check that all fields are filled
        elif all([node_type, edge_type]):
            if (node_type is not None) & (edge_type != self.r.get(node_type)):
                raise TypeError('The adjacent node type and edge type do not describe proper connection')

            adjacent_nodes = list(self.r.smembers(f'{edge_type}:<{name}>'))
        else:
            raise Exception('Fields are only partially filled in')
        return adjacent_nodes

    def get_recommendations(self, name: str) -> List[str]:
        """
        Get book recommendations for a given person,
        excluding books they already have.

        Args:
        name: str, the person to find recommendations for.

        Returns:
        recommended_books: List[str], list of books.
        """
        people_they_know = self.get_adjacent(name, node_type='Person', edge_type='knows')
        books_they_bought = set(self.get_adjacent(name, node_type='Book', edge_type='bought'))
        other_ppl_books = set([])
        # get the books that other people have bought
        for i in people_they_know:
            other_ppl_books = other_ppl_books.union(set(self.get_adjacent(i, node_type='Book', edge_type='bought')))
        recommended_books = other_ppl_books.difference(books_they_bought)
        return recommended_books
