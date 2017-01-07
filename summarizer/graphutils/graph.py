class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = {}

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges[(edge.first_vertex, edge.second_vertex)] = edge

    def find_edge(self, first_vertex, second_vertex):
        res = self.edges.get((first_vertex, second_vertex), None)
        return res if res else self.edges.get((second_vertex, first_vertex), None)

