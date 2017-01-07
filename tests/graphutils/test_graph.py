import unittest

from summarizer.graphutils.vertex import Vertex
from summarizer.graphutils.graph import Graph
from summarizer.graphutils.edge import Edge


class GraphTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_add_vertex(self):
        vertex = Vertex("sample", ["sample"])
        self.graph.add_vertex(vertex)
        self.assertTrue(vertex in self.graph.vertices)

    def test_add_edge(self):
        vertex1 = Vertex("sample", ["sample"])
        vertex2 = Vertex("sample", ["sample"])
        edge = Edge(vertex1, vertex2, 1)
        self.graph.add_edge(edge)
        self.assertTrue(len(self.graph.edges) == 1)
        self.assertTrue(edge in self.graph.edges.values())

    def test_find_edge_existing(self):
        vertex1 = Vertex("sample", ["sample"])
        vertex2 = Vertex("sample", ["sample"])
        edge = Edge(vertex1, vertex2, 4)
        self.graph.add_edge(edge)
        self.assertIsNotNone(self.graph.find_edge(vertex1, vertex2))
        self.assertIsNotNone(self.graph.find_edge(vertex2, vertex1))

    def test_find_edge_non_existing(self):
        vertex1 = Vertex("sample", ["sample"])
        vertex2 = Vertex("sample", ["sample"])
        vertex3 = Vertex("sample", ["sample"])
        edge = Edge(vertex1, vertex2, 9)
        self.graph.add_edge(edge)
        self.assertIsNone(self.graph.find_edge(vertex1, vertex3))

    def test_find_edge_isolated_vertices(self):
        vertex1 = Vertex("sample", ["sample"])
        vertex2 = Vertex("sample", ["sample"])
        self.graph.add_vertex(vertex1)
        self.graph.add_vertex(vertex2)
        self.assertIsNone(self.graph.find_edge(vertex2, vertex1))
