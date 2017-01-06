import unittest

from summarizer.graphutils.vertex import Vertex


class VertexTestCase(unittest.TestCase):

    def setUp(self):
        self.vertex = Vertex("sample text common word", ["sample", "text", "common", "word"])
        self.vertex2 = Vertex("sample2 text2 common word", ["sample2", "text2", "common", "word"])

    def test_similarity(self):
        self.assertTrue(self.vertex.similarity(self.vertex2) == 1.660964047443681)

    def test_common_words(self):
        common_words = self.vertex._common_words(self.vertex2)
        self.assertTrue("common" in common_words)
        self.assertTrue("word" in common_words)
        self.assertTrue(len(common_words) == 2)

    def test_increment_degree(self):
        self.vertex.increment_degree()
        self.assertEqual(self.vertex.degree, 1)
        self.vertex.increment_degree()
        self.assertEqual(self.vertex.degree, 2)

    def test_add_neighbour(self):
        self.vertex.add_neighbour(self.vertex2)
        self.assertTrue(self.vertex2 in self.vertex.neighbours)
