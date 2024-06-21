import networkx as nx
import matplotlib.pyplot as plt
import folium
import pandas as pd
import random


class LondonNetworkGraph:
    def __init__(self):
        self.graph = nx.DiGraph()  # Armazenar o grafo
        self.stations_data = {}  # Dicionário com as informacoes de cada estacao
        self.connections_data = {} # Dicionario com todas as informacao de cada connection

    def stations(self, file_path):
        stations_df = pd.read_csv(file_path, delimiter=';')  # Ler o ficheiro
        for _, station in stations_df.iterrows():  # Iterar informacao de cada estacao
            node_data = {
                'latitude': station['latitude'],
                'longitude': station['longitude'],
                'name': station['name'],
                'zone': station['zone'],
                'total_lines': station['total_lines'],
                'rail': station['rail']
            }
            self.graph.add_node(station['id'], **node_data)  # Armazenar no dicionario
            self.stations_data[station['id']] = node_data  # utilizar o id como chave

    def connections(self, file_path):
        connections_df = pd.read_csv(file_path, delimiter=';')
        for _, connection in connections_df.iterrows():  # Iterar informacao de cada connection
            edge_data = {
                'line': connection['line'],
                'weight': connection['weight'],
                'off_peak': connection['off_peak'],
                'am_peak': connection['am_peak'],
                'inter_peak': connection['inter_peak']
            }
            self.graph.add_edge(connection['from_id'], connection['to_id'], **edge_data)  # Armazenar no dicionario
            self.connections_data[(connection['from_id'], connection['to_id'])] = edge_data  # Utilizar o id como chave

    def n_stations(self):
        return len(self.graph.nodes())

    def n_stations_zone(self):
        stations_per_zone = {}  # criar um dicionario vazio

        for node_id, node_data in self.stations_data.items():  # obter os nodes do graph
            zone = node_data['zone']

            if zone in stations_per_zone:  # Confirmar se o node esta no dicionario e caso nao esteja adicionar
                stations_per_zone[zone] += 1
            else:
                stations_per_zone[zone] = 1

        stations_zone_ordenado = dict(sorted(stations_per_zone.items()))  # ordenar o dicionario

        return stations_zone_ordenado

    def n_edges(self):
        return len(self.graph.edges())

    def n_edges_line(self):
        edge_line = {}

        for _, edge_data in self.connections_data.items():
            line = edge_data['line']

            if line in edge_line:
                edge_line[line] += 1
            else:
                edge_line[line] = 1

        return edge_line

    def mean_degree(self):
        num_nodes = len(self.graph.nodes)
        total_degree = sum(self.graph.out_degree(node) for node in self.graph.nodes)

        return round(total_degree / num_nodes, 2) if num_nodes != 0 else 0

    def mean_weight(self):
        weights = []
        for edge_data in self.connections_data.values():  # dados das 3 colunas em uma lista
            weights_1 = edge_data['off_peak']
            weights_2 = edge_data['am_peak']
            weights_3 = edge_data['inter_peak']
            weights.append((weights_1 + weights_2 + weights_3) / 3)
        mean_weight = round(sum(weights) / len(weights), 2)
        return mean_weight

    def visualize(self):  # vizualizar o graph
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        plt.show()

    def visualize_map(self, shortest_path=None):  # vizualizar o graph no mapa
        m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
        for node, data in self.graph.nodes(data=True):
            folium.Marker([data['latitude'], data['longitude']], popup=data['name']).add_to(m)
        for edge in self.graph.edges():
            start = self.graph.nodes[edge[0]]
            end = self.graph.nodes[edge[1]]
            folium.PolyLine([(start['latitude'], start['longitude']), (end['latitude'], end['longitude'])],
                            color='red').add_to(m)

        if shortest_path: # Destacar o caminho mais curto, se fornecido
            for i in range(len(shortest_path) - 1):
                start_node = shortest_path[i]
                end_node = shortest_path[i + 1]
                start = self.graph.nodes[start_node]
                end = self.graph.nodes[end_node]
                folium.PolyLine([(start['latitude'], start['longitude']), (end['latitude'], end['longitude'])],
                                color='blue', weight=5).add_to(m)
        return m

    def dijkstra_net(self):  # implementar Dijkstra com NetworkX
        source = random.randint(1, graph.n_stations())
        target = random.randint(1, graph.n_stations())
        shortest_path = nx.dijkstra_path(self.graph, source, target)
        return shortest_path

    def dijkstra(self, source, target):  # Dijkstra sem NetworkX
        # inicio dos valores
        distances = {node_id: float('inf') for node_id in self.graph.nodes}  # lista de distancias
        previous = {node_id: None for node_id in self.graph.nodes}  # nodes anteriores
        distances[source] = 0
        unvisited = set(self.graph.nodes)  # nodes nao visitados

        while unvisited:
            # no com menor distancia
            min_distance = float('inf')  # encontrar node com menor distancia atual
            min_node = None
            for node in unvisited:  # encontrar node com menor distancia atual
                if distances[node] < min_distance:
                    min_distance = distances[node]
                    min_node = node

            if min_node == target:
                break

            unvisited.remove(min_node)  # atualizar lista unvisited

            # atualizar distancia dos vizinhos
            for neighbor in self.graph.neighbors(min_node):
                edge_data = self.connections_data[(min_node, neighbor)]
                weight = edge_data['weight']
                total_distance = distances[min_node] + weight

                if total_distance < distances[neighbor]:
                    distances[neighbor] = total_distance
                    previous[neighbor] = min_node

        # caminho mais curto
        shortest_path_ = []
        current_node = target
        while current_node is not None:
            shortest_path_.insert(0, current_node)
            current_node = previous[current_node]

        return shortest_path_


# inserir os ficheiros

graph = LondonNetworkGraph()
graph.stations('stations_clean.csv')
graph.connections('conects.csv')

# n_stations
n_stations = graph.n_stations()
print('-' * 10, 'NÚMERO ESTAÇÕES', '-' * 10)
print(f'O número de estações é {n_stations}')
print('-' * 42)

# n_stations_zone
count_station_zone = graph.n_stations_zone()
print('-' * 10, 'ESTAÇÕES POR ZONA', '-' * 10)
for zone, count in count_station_zone.items():
    print(f'Zona {zone}: {count} estações')
print('-' * 42)

# n_edges
n_edges = graph.n_edges()
print('-' * 10, 'NÚMERO EDGES', '-' * 10)
print(n_edges)
print('-' * 42)

# n_edges_line
count_edge_line = graph.n_edges_line()
print('-' * 10, 'NÚMERO EDGES/LINE', '-' * 10)
for line, contagem in count_edge_line.items():
    print(f'Linha {line}: {contagem} edges')
print('-' * 42)

# mean_degree
mean_degree = graph.mean_degree()
print('-' * 10, 'MEAN DEGREE', '-' * 10)
print(f'Média dos graus: {mean_degree}')
print('-' * 42)

# mean_weight
mean_weight = graph.mean_weight()
print('-' * 10, 'MEAN WEIGHT', '-' * 10)
print(mean_weight)

# vizualize
m = graph.visualize_map()
m.save('map.html')
print('-' * 10, 'SHORTEST PATH', '-' * 10)
shortest_path = graph.dijkstra_net()
print(shortest_path)
print('-' * 42)
m = graph.visualize_map(shortest_path)
m.save('dijkstra.html')

# dijkstra python
source_node = random.randint(1, graph.n_stations())
target_node = random.randint(1, graph.n_stations())
shortest_path_ = graph.dijkstra(source_node, target_node)
print(f'O caminho mais curto é: {shortest_path_}')
m = graph.visualize_map(shortest_path_)
m.save('dijkstrapython.html')
