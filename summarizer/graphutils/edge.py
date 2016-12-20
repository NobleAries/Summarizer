class Edge:

    def __init__(self, first_vertex, second_vertex, weight):
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.weight = weight
        self.first_vertex.increment_degree()
        self.second_vertex.increment_degree()
        self.first_vertex.add_neighbour(second_vertex)
        self.second_vertex.add_neighbour(first_vertex)