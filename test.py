import json

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
        self.distances = {}

        self.reverse_edges = defaultdict(list)
        self.reverse_distances = {}

        self.reverse = False

    def set_reverse(self, value):
        if isinstance(value, bool):
            self.reverse = value

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        if not(from_node in self.nodes or to_node in self.nodes): return False

        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance

        self.reverse_edges[to_node].append(from_node)
        self.reverse_distances[(to_node, from_node)] = distance
        return True

    def neighbours(self, node):
        return self.reverse_edges[node] if self.reverse else self.edges[node]

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
            if neighbour not in path_so_far:
                path = self.find_paths_with_cycles(path_so_far + [neighbour])
                all_paths.extend(path)

        return all_paths

    def route_weight(self, route):
        if len(route) < 2: return 0

        total_weight = 0
        for x in xrange(len(route)-1):
            node = route[x]
            next_node = route[x+1]
            weight = self.reverse_distances[(node, next_node)] if self.reverse else self.distances[(node, next_node)]
            total_weight += weight

        return total_weight

carpool = Graph()

car_num = 3
cars = ['car'+str(x) for x in xrange(car_num)]
home_num = 3
homes = ['home'+str(x) for x in xrange(home_num)]
dest = ['dest']


for x in cars+homes+dest:
    carpool.add_node(x)

for node in cars:
    for other in homes+dest:
        rand = randint(1,10)
        carpool.add_edge(node, other, rand)

for node in homes:
    for other in homes+dest:
        if node != other:
            rand = randint(1,10)
            carpool.add_edge(node, other, rand)

carpool.set_reverse(True)
routes = carpool.find_all_paths('dest')

print
print 'weights:'

weights = {}
track = {}

def str2int(string):
    return sum([ord(l) for l in list(string)])

for route in routes:
    weight = carpool.route_weight(route)

    route_num = [str2int(x) for x in route]
    mul = reduce(lambda x, y: x*y, route_num)
    add = sum(route_num)
    identity = mul*add

    if track.has_key(identity):
        value = track[identity][1]
        if weight < value:
            track[identity] = [route, weight]
    else:
        track[identity] = [route, weight]

for k,v in track.iteritems():
    weights[tuple(v[0])] = v[1]

print weights

filtered_routes = [list(x) for x in weights.keys()]

def subset_sum(numbers, target, partial=[]):
    subsets = []
    s = sum(partial)

    if s == target: 
        return [partial]
    elif s > target:
        return []

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subsets.extend(subset_sum(remaining, target, partial + [n]))
    return subsets

target = 0
for node in cars+homes:
    val = str2int(node)
    print node
    print val
    target += val

num_routes = []
for route in filtered_routes:
    temp_route = route[1:]
    print temp_route
    val = sum([str2int(x) for x in temp_route])
    num_routes.append(val)

print target
print num_routes

subsets = subset_sum(num_routes, target)
print subsets
