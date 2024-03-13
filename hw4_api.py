"""
Ceara Zhang
DS 4300
HW 4 Graph Data Models
Created: 10 March 2024
Updated: 12 March 2024

hw4_api.py:
A Python module designed to facilitate graph
data management and traversal within a Redis database. This API provides a set
of methods for creating, querying, and modifying graph structures stored in Redis.
"""

import redis
from typing import List


class GraphModel:

    def __init__(self, port: int):
        """
        Create connection with Redis
        """
        self.r = redis.Redis('localhost', port, decode_responses=True)

    def close(self):
        """
        Close connection to Redis.
        """
        self.r.close()

    def destroy_database(self):
        """
        Destroy the database for rerunning purposes.
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
        # if node_id doesn't exist, set one for auto incrementation
        if self.r.exists('node_id'):
            node_id = int(self.r.get('node_id'))
        else:
            self.r.set('node_id', 0)
            node_id = int(self.r.get('node_id'))
        # create node
        self.r.set(f'node:<{name}>', node_id)
        # set node's type
        self.r.set(f'type:<{node_id}>', type)
        # note the types of nodes in list
        self.r.sadd('node_type_list', type)
        # autoincrement
        self.r.incr('node_id')

    def get_node_type(self, node: str) -> str:
        """
        Get type of node.

        Args:
        node: str, the node to find type information of

        Returns:
        node_type: str, the node's type.
        """
        node_id = int(self.r.get(f'node:<{node}>'))
        node_type = str(self.r.get(f'type:<{node_id}>'))
        return node_type

    def add_edge(self, name1: str, name2: str, type: str):
        """
        Establishes a connection between two nodes by adding an edge.
        Unique edge connection types are recorded.

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
        Retrieve the names of adjacent nodes. Optionally filter by node and/or edge type.

        Args:
        name: str, the target node to find adjacent connections.
        node_type: str or None, the desired type of adjacent node.
        edge_type: str or None, the desired type of edge connection.

        Returns:
        List[str]: A list of adjacent node names.
        """
        if node_type is None and edge_type is None:
            # Retrieve adjacent nodes if no type filters are specified
            adjacent_nodes = set([])
            for edge_type in self.r.smembers('edge_type_list'):
                adjacent_nodes |= set(self.r.smembers(f'{edge_type}:<{name}>'))
            return list(adjacent_nodes)

        elif all([node_type, edge_type]):
            # Retrieve adjacent nodes filtered by both node and edge type
            if edge_type != self.r.get(node_type):
                raise TypeError('The specified node type and edge type do not match.')
            return list(self.r.smembers(f'{edge_type}:<{name}>'))

        else:
            # Raise exception if only one filter is specified
            raise ValueError('Both node type and edge type must be provided or omitted together.')

    def get_recommendations(self, name: str) -> List[str]:
        """
        Retrieve book recommendations for a specified person, excluding books they already own.

        Args:
        name: str, the person for whom recommendations are sought.

        Returns:
        List[str]: A list of recommended books.
        """
        # Get the list of people the specified person knows
        ppl_they_know = self.get_adjacent(name, node_type='Person', edge_type='knows')

        # Get the set of books the specified person has already bought
        books_they_bought = set(self.get_adjacent(name, node_type='Book', edge_type='bought'))

        # Initialize an empty set to store books bought by people they know
        other_ppl_books = set([])

        # Iterate through each person they know to collect books they bought
        for person in ppl_they_know:
            other_ppl_books |= set(self.get_adjacent(person, node_type='Book', edge_type='bought'))

        # Get the set of books recommended to the specified person (excluding those they already own)
        recommended_books = other_ppl_books - books_they_bought

        return list(recommended_books)

