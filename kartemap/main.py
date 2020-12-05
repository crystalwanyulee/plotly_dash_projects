
import os
os.chdir('C://Users/admin/Documents/Python2/kartemap')
import pathlib

from algorithms.shortest_path import Dijkstra
from graph.network import Network
import numpy as np
from itertools import permutations


def read_network_from_file(file_name, delimeter=','):
    """ Read from a file and build a network
    file_name: file to read from
    delimeter: delimeter that separates fields
    """
    cities = list()
    distances = dict()

    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        fields = line.rstrip().split(delimeter)
        city_1 = fields[0].strip(' ')
        city_2 = fields[1].strip(' ')
        distance = float(fields[2])

        # build the list of cities
        if city_1 not in cities:
            cities.append(city_1)
        if city_2 not in cities:
            cities.append(city_2)

        # build the dictionary based on city distances
        if cities.index(city_1) not in distances.keys():
            distances[cities.index(city_1)] = {cities.index(city_2): distance}
        if cities.index(city_2) not in distances[cities.index(city_1)].keys():
            distances[cities.index(city_1)][cities.index(city_2)] = distance

    return cities, distances


def shortes_path(start_node, target_node):
    # read network from file
    file_name = 'data/network_distance.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # using Dijkstra's algorithm, compute least cost (distance)
    # from start city to all other cities
    Dijkstra.compute(network, network.get_node(start_node))

    # show the shortest path(s) from start city to all other cities
    
    target_city = network.get_node(target_node)
    path = [target_city.get_name()]
    Dijkstra.compute_shortest_path(target_city, path)
    
    return path[::-1], target_city.get_weight()

def shortest_path(start_node, target_node):
    # read network from file
    file_name = 'data/airport_distance.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # using Dijkstra's algorithm, compute least cost (distance)
    # from start city to all other cities
    Dijkstra.compute(network, network.get_node(start_node))

    # show the shortest path(s) from start city to all other cities
    
    target_city = network.get_node(target_node)
    path = [target_city.get_name()]
    Dijkstra.compute_shortest_path(target_city, path)
    
    return path[::-1], round(target_city.get_weight())

def best_path(start_node, target_node, intermediary_nodes=[]):
    
    nodes_list = [start_node] + intermediary_nodes + [target_node]
    nodes = []
    route = []
    total_dist = 0
    for i in range(len(nodes_list)-1):
        path, dist = shortest_path(nodes_list[i], nodes_list[i+1])
        total_dist += dist
        if i == 0:
            route.extend(path)
            path = [0]*len(path)
            path[0] = 1
            path[-1] = 1
            nodes.extend(path)
        else:
            route.extend(path[1:])
            path = [0]*len(path)
            path[0] = 1
            path[-1] = 1
            nodes.extend(path[1:])
            
    return nodes, route, total_dist


def best_route_planner(nodes_list, start_fixed=True, end_fixed=True):

    best_nodes = []
    best_route = None
    shortest_dist = np.Inf
    comb_list = nodes_list
    
    if start_fixed:
        comb_list = comb_list[1:]
        
    if end_fixed:
        comb_list = comb_list[:-1]

 #   print(comb_list)
    combinations = []
    for order in permutations(comb_list, len(comb_list)):
        order = list(order)
        if start_fixed:
            order = [nodes_list[0]] + order
            
        if end_fixed:
            order = order + [nodes_list[-1]]
        
        if (order not in combinations) & (order[::-1] not in combinations):
            combinations.append(order)
     #       print('Combination:', order)
            nodes, route, dist = best_path(order[0], order[-1], order[1:-1])
          #  print('Route', route,'\n', 'Dist', dist)
            if dist < shortest_dist:
                shortest_dist = dist
                best_route = route
                best_nodes = nodes

    return best_nodes, best_route, shortest_dist



if __name__ == '__main__':
    nodes_list = ['Baltimore', 'Dallas']

    print(best_path(nodes_list[0], nodes_list[1]))
    print(best_route_planner(nodes_list))
    
    nodes_list = ['Portland', 'Dallas', 'Minneapolis', 'Los Angeles']

    print(best_route_planner(nodes_list))
    print(best_route_planner(nodes_list, start_fixed=False))
    print(best_route_planner(nodes_list, end_fixed=False))
    print(best_route_planner(nodes_list, start_fixed=False, end_fixed=False))
