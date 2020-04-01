import sys
from functools import total_ordering


@total_ordering
class Vertex:
    def __init__(self, node, lon, lat, type):
        self.lon = lon
        self.lat = lat
        self.id = node
        self.type = type
        self.h = 0
        self.g = sys.maxsize
        self.f = self.h + self.g
        self.t = sys.maxsize
        self.adjacent = {}
        self.visited = False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.g == other.g
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.g < other.g
        return NotImplemented

    def __hash__(self):
        return id(self)

    def add_neighbor(self, name, mode, neighbor, weight=0): #adds neighbor node data with edge weight, name and mode
        self.adjacent[neighbor] = [weight, name, mode]

    def get_connections(self): #returns neighbor nodes of current node obj
        return self.adjacent.keys()

    def get_id(self): #returns node name
        return self.id

    def get_weight(self, neighbor): #returns neigbor node weight
        return self.adjacent[neighbor][0]

    def get_name(self, neighbor): #returns neigbor node name
        return self.adjacent[neighbor][1]

    def get_mode(self, neighbor): #returns neigbor node mode
        return self.adjacent[neighbor][2]

    def get_node_type(self):
        return self.type

    def set_g(self, g): #sets node g value
        self.g = g

    def get_g(self): #returns nodes g value
        return self.g

    def set_t(self, t): #sets node t value
        self.t = t

    def get_t(self): #returns nodes t value
        return self.t


    def get_lon(self): #returns node longitude data
        return self.lon

    def get_lat(self): #returns node latitude data
        return self.lat

    def set_h(self, h):  #sets node h value
        self.h = h

    def get_h(self): #return nodes h value
        return self.h

    def set_f(self, f): #sets node f value
        self.f = f

    def get_f(self): #returns node f value
        return self.f

    def set_visited(self): #sets node to be visited
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, lon, lat, type): #adds vertext to vert dict
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, lon, lat, type)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):#returns vertexs
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, name, mode, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)  # throw error instead? TBC
        if to not in self.vert_dict:
            self.add_vertex(to)  # throw error instead? TBC

        if mode == 'walk': #if mode is walking set edges to be bidirectional
            self.vert_dict[frm].add_neighbor(name, mode, self.vert_dict[to], cost)
            self.vert_dict[to].add_neighbor(name, mode, self.vert_dict[frm], cost)
        else: #else set it to be directed edge by setting other direction to have 'infinite' weight
            self.vert_dict[frm].add_neighbor(name, mode, self.vert_dict[to], cost)
            self.vert_dict[to].add_neighbor(name, mode, self.vert_dict[frm], sys.maxsize)

    def get_vertices(self):
        return self.vert_dict.keys()
