import math


class Vertex:

    def __init__(self, sentence, words):
        self.sentence = sentence
        self.words = words
        self.degree = 0
        self.neighbours = []

    def similarity(self, other_vertex):
        number_of_common_words = len(self._common_words(other_vertex))
        scale_factor = math.log10(len(self.words)) + math.log10(len(other_vertex.words))
        return number_of_common_words / scale_factor

    def _common_words(self, other_vertex):
        return set(self.words) & set(other_vertex.words)

    def increment_degree(self):
        self.degree += 1

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
