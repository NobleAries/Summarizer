class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges.append(edge)

    def find_edge(self, first_vertex, second_vertex):
        for edge in self.edges:
            if (edge.first_vertex == first_vertex and edge.second_vertex == second_vertex or
                    edge.second_vertex == first_vertex and edge.first_vertex == second_vertex):
                return edge
        return None
