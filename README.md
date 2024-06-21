# London Network Graph

## Overview

The London Network Graph project is a Python-based analysis and visualization tool for London's transport network. This project utilizes NetworkX for graph data structure manipulation, Matplotlib for simple graph visualization, and Folium for interactive map visualization. It processes data from CSV files to create a graph representing stations and connections in the London transport network, and provides functionalities to analyze various network properties as well as find shortest paths using Dijkstra's algorithm.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methods and Functions](#methods-and-functions)
- [Visualization](#visualization)
- [Examples](#examples)
- [Data Files](#data-files)
- [License](#license)

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/london-network-graph.git
    ```

2. Navigate to the project directory:

    ```bash
    cd london-network-graph
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have the necessary CSV data files: `stations_clean.csv` and `conects.csv`.
2. Create an instance of the `LondonNetworkGraph` class.
3. Load the stations and connections data using the `stations` and `connections` methods.
4. Use the various methods to analyze and visualize the network.

## Project Structure

```plaintext
LondonNetworkGraph/
├── london_network_graph.py   # The main class implementation
├── stations_clean.csv        # CSV file with station data
├── conects.csv               # CSV file with connection data
├── map.html                  # Generated map visualization
├── dijkstra.html             # Generated map with shortest path visualization
├── dijkstrapython.html       # Generated map with Dijkstra's algorithm visualization
├── README.md                 # This readme file
├── requirements.txt          # List of dependencies
└── examples/                 # Example scripts and notebooks

## Methods and Functions

### LondonNetworkGraph

- `stations(file_path)`: Load station data from a CSV file.
- `connections(file_path)`: Load connection data from a CSV file.
- `n_stations()`: Get the number of stations in the graph.
- `n_stations_zone()`: Get the number of stations per zone.
- `n_edges()`: Get the number of edges (connections) in the graph.
- `n_edges_line()`: Get the number of edges per line.
- `mean_degree()`: Calculate the mean degree of the graph.
- `mean_weight()`: Calculate the mean weight of the edges.
- `visualize()`: Visualize the graph using Matplotlib.
- `visualize_map(shortest_path=None)`: Visualize the graph on a map using Folium, with optional shortest path highlighting.
- `dijkstra_net()`: Find the shortest path using NetworkX's Dijkstra implementation.
- `dijkstra(source, target)`: Find the shortest path using a custom Dijkstra implementation.

## Visualization

- **Matplotlib**: Used for basic graph visualization.
- **Folium**: Used for interactive map visualization, highlighting stations and connections, and optionally showing the shortest path.

## Data Files

- **stations_clean.csv**: Contains station data with columns for ID, latitude, longitude, name, zone, total lines, and rail.
- **conects.csv**: Contains connection data with columns for from_id, to_id, line, weight, off_peak, am_peak, and inter_peak.
