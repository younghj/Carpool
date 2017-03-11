# import json

# with open('directions2.txt') as f:
    # data = json.load(f)[0]

# print len(data)
# print data.keys()
# print data['waypoint_order']
# print

# legs = data['legs']


# for leg in legs:
    # print leg.keys()
    # print leg['start_address']
    # print leg['end_address']
    # print leg['duration']
    # print leg['distance']
    # print

# class Node(object):
    # def __init__(self, t='', n=''):
        # self.type = t #car, home, dest
        # self.name = n.replace(' ','_')
        # # self.options = [] #toll(car), transit(home)

    # def get_name(self, orig = False):
        # return orig if self.name.replace('_',' ') else self.name

from collections import defaultdict
import string
from random import randint

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.reverse_edges = defaultdict(list)
        self.distances = {}
        self.reverse_distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        if not(from_node in self.nodes or to_node in self.nodes): return False

        self.edges[from_node].append(to_node)
        self.reverse_edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.reverse_distances[(to_node, from_node)] = distance
        return True

    def neighbours(self, node):
        return self.edges[node]

    def node_num(self):
        return len(list(self.nodes))

    def index(self, num):
        try:
            value = list(self.nodes)[num]
        except IndexError:
            value = ''
        return value

    def find_all_paths(self, start):
        if start in self.nodes:
            return self.find_paths_with_cycles([start])
        return []

    def find_paths_with_cycles(self, path_so_far):
        all_paths = []
        last_node = path_so_far[-1]
        neighbours = self.neighbours(last_node)

        if not len(neighbours):
            return [path_so_far]

        for neighbour in neighbours:
            if neighbour in path_so_far:
                return [path_so_far]
            else:
                path = self.find_paths_with_cycles(path_so_far + [neighbour])
                all_paths.extend(path)

        return all_paths


#init graph
upper = list(string.ascii_uppercase)[:5]
test = Graph()
for letter in upper:
    test.add_node(letter)

#make random graph
nodes = list(test.nodes)
for node in nodes:
    for other in nodes:
        if node == other: continue
        rand = randint(-5,5)
        if rand > 0:
            test.add_edge(node, other, rand)

print test.distances

a = test.find_all_paths('A')
print 'res'
print a

# reverse 
# don't use dijsktra
# instead get find_all_paths from dest to each car
# def shortest(graph, initial): #dijsktra
    # visited = {initial: 0}
    # path = {}

    # nodes = set(graph.nodes)

    # while nodes:
        # min_node = None
        # for node in nodes:
            # if node in visited:
                # if min_node is None:
                    # min_node = node
                # elif visited[node] < visited[min_node]:
                    # min_node = node
        # if min_node is None:
            # break

        # nodes.remove(min_node)
        # current_weight = visied[min_node]

        # for edge in graph.edges[min_node]:
            # weight = current_weight + graph.distance[(min_node, edge)]
            # if edge not in visited or weight < visited[edge]:
                # visited[edge] = weight
                # path[edge] = min_node

    # return visited, path

# class Carpool(object):
    # def __init__(self):
        # self.cars = []
        # self.homes = []
        # self.dest = []
        # self.edges = {}

    # def set_car(self, cars):
        # for car in cars:
            # node = Node('car',car)
            # self.cars.append(node)

    # def set_homes(self, homes):
        # for home in homes:
            # node = Node('home',home)
            # self.homes.append(node)

    # def set_dest(self, dest):
        # node = Node('dest',dest)
        # self.dest.append(node)

    # def make(self):
        # for node in self.cars:
            # for other in self.homes + self.dest:
                # key = node.get_name() + ' ' + other.get_name()
                # self.edges[key] = 0
        # for node in self.homes:
            # for other in self.homes + self.dest:
                # if not(node is other):
                    # key = node.get_name() + ' ' + other.get_name()
                    # self.edges[key] = 0

