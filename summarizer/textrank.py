from .summarize import SummarizationAlgorithm
from .nlp import NaturalLanguageProcessor
from .graphutils.graph import Graph
from .graphutils.vertex import Vertex
from .graphutils.edge import Edge


class TextRankAlgorithm(SummarizationAlgorithm):

    def execute(self, text, number_of_sentences):
        sentences, words_in_sentences = self._prepare_sentences_and_words(text)
        self._create_sentence_graph(sentences, words_in_sentences)
        scores = self._pagerank()
        return self._process_results(scores, number_of_sentences)

    @staticmethod
    def _prepare_sentences_and_words(text):
        sentences = NaturalLanguageProcessor.split_by_sentences(text)
        words_in_sentences = {sentence: NaturalLanguageProcessor.split_by_words(sentence) for sentence in sentences}
        words_in_sentences = {sentence: words for sentence, words in words_in_sentences.items() if len(words) > 1}
        sentences = words_in_sentences.keys()
        return sentences, words_in_sentences

    def _create_sentence_graph(self, sentences, words):
        self.graph = Graph()
        self._add_vertices(sentences, words)
        self._add_edges()

    def _add_vertices(self, sentences, words):
        for sentence in sentences:
            self.graph.add_vertex(Vertex(sentence, words[sentence]))

    def _add_edges(self):
        for index, first_vertex in enumerate(self.graph.vertices):
            for _, second_vertex in enumerate(self.graph.vertices, index + 1):
                similarity = first_vertex.similarity(second_vertex)
                self.graph.add_edge(Edge(first_vertex, second_vertex, similarity))

    def _pagerank(self, damping_factor=0.85, max_iterations=100, convergence_limit=10e-3):
        init_val = 1.0 / len(self.graph.vertices)
        scores = dict.fromkeys(self.graph.vertices, init_val)

        for _ in range(max_iterations):
            converged_vertices = 0
            for vertex_i in self.graph.vertices:
                rank = 1 - damping_factor
                for vertex_j in vertex_i.neighbours:
                    rank += (damping_factor * self.graph.find_edge(vertex_j, vertex_i).weight * scores[vertex_j] /
                             sum(self.graph.find_edge(vertex_j, vertex_k).weight for vertex_k in vertex_j.neighbours))
                if abs(scores[vertex_i] - rank) < convergence_limit:
                    converged_vertices += 1

                scores[vertex_i] = rank

            if converged_vertices == len(self.graph.vertices):
                break

        return scores

    @staticmethod
    def _process_results(scores, number_of_sentences):
        sorted_results = sorted(scores, key=scores.get, reverse=True)
        return '\n'.join(vertex.sentence for vertex in sorted_results[:number_of_sentences])

