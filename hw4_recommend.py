"""
Ceara Zhang and Julia Geller
DS 4300
Graph Data Models
Created: 10 March 2024
Updated: 12 March 2024

hw4_recommend.py:
implements a recommendation engine. It establishes connections to a Redis server,
creates the nodes and edges, and generates personalized book recommendations
for individuals.
"""

from hw4_api import GraphModel


def main():
    # Establish connection to Redis Server
    api = GraphModel(6379)

    # destroy existing database if any
    api.destroy_database()

    # create person nodes
    api.add_node('Brendan', 'Person')
    api.add_node('Emily', 'Person')
    api.add_node('Paxtyn', 'Person')
    api.add_node('Spencer', 'Person')
    api.add_node('Trevor', 'Person')

    # create book nodes
    api.add_node('Cosmos', 'Book')
    api.add_node('Database Design', 'Book')
    api.add_node('DNA and You', 'Book')
    api.add_node('The Life of Cronkite', 'Book')

    # create edges
    api.add_edge('Brendan', 'Database Design', 'bought')
    api.add_edge('Brendan', 'DNA and You', 'bought')
    api.add_edge('Emily', 'Spencer', 'knows')
    api.add_edge('Emily', 'Database Design', 'bought')
    api.add_edge('Paxtyn', 'Database Design', 'bought')
    api.add_edge('Paxtyn', 'The Life of Cronkite', 'bought')
    api.add_edge('Spencer', 'Emily', 'knows')
    api.add_edge('Spencer', 'Brendan', 'knows')
    api.add_edge('Spencer', 'Cosmos', 'bought')
    api.add_edge('Spencer', 'Database Design', 'bought')
    api.add_edge('Trevor', 'Database Design', 'bought')
    api.add_edge('Trevor', 'Cosmos', 'bought')

    # book recommendations for Spencer
    recommendations = api.get_recommendations('Spencer')
    print(recommendations)

    # Close Redis Connection
    api.close()


if __name__ == '__main__':
    main()
