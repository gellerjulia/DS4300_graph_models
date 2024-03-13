# Graph Data Models for Recommendation Engine

This repository contains Python scripts implementing a recommendation engine based on graph data models using the GraphModel API for Redis. 
The recommendation engine utilizes graph structures to provide personalized book recommendations for individuals, leveraging their social 
connections and purchasing history.

## Files

### 1. `hw4_recommend.py`

#### Description:
- **Authors:** Ceara Zhang and Julia Geller
- **Created:** 10 March 2024
- **Updated:** 13 March 2024
- **Purpose:** Recommendation Engine

#### Functionality:
- Establishes a connection to the Redis server using the GraphModel API.
- Creates nodes representing people (persons) and books in the graph.
- Establishes relationships (edges) between nodes to indicate purchases and social connections.
- Generates personalized book recommendations for a specific individual based on their social network and purchasing history.
- Displays the recommendations to the user.

### 2. `recommend.py`

#### Description:
- **Authors:** Ceara Zhang and Julia Geller
- **Created:** 10 March 2024
- **Updated:** 13 March 2024
- **Purpose:** Driver Script for Recommendation Engine

#### Functionality:
- Serves as a driver for the recommendation engine implemented in `hw4_recommend.py`.
- Utilizes the GraphModel API for Redis to create a sample graph dataset, simulate user interactions, and obtain book recommendations for a specified individual.
- Creates a sample graph dataset consisting of people and books, along with their relationships.
- Invokes the recommendation engine to generate personalized book recommendations for a specific individual.
- Displays the recommendations to the user.

## Requirements
- Python 3.7+
- Redis server
- Redis Python library

## Usage
1. Install the required Python libraries (redis, typing)
2. Ensure Redis server is running locally or update connection details in the scripts.
3. Execute `hw4_recommend.py` to generate book recommendations based on the sample graph dataset.
4. Execute `recommend.py` to drive the recommendation engine and display recommendations.

## Author and Contributions
- Julia Geller was responsible for writing SQL queries and generating their corresponding results for the given graph data.
- Ceara Zhang was responsible for creating the API for storing graphs in Redis, and demonstrated the methods by re-building the graph data and giving a reccomendation to Spencer.
