import unittest

from summarizer.textrank import TextRankAlgorithm
from summarizer.graphutils.graph import Graph
from summarizer.nlp import NaturalLanguageProcessor


class TextRankTestCase(unittest.TestCase):
    def setUp(self):
        self.textrank = TextRankAlgorithm()
        self.sentences = ["Sentence 1", "Sentence 1", "Sentence 2", "Sentence 3"]
        self.words = {sentence: NaturalLanguageProcessor.split_by_words(sentence) for sentence in self.sentences}

    def test_add_vertices(self):
        self.textrank.graph = Graph()
        self.textrank._add_vertices(self.sentences, self.words)
        self.assertTrue(len(self.textrank.graph.vertices) == len(self.sentences))

    def test_add_edges(self):
        self.textrank.graph = Graph()
        self.textrank._add_vertices(self.sentences, self.words)
        self.textrank._add_edges()
        self.assertIsNotNone(self.textrank.graph.edges)
        self.assertTrue(len(self.textrank.graph.edges) > 0)

    def test_create_sentence_graph(self):
        self.textrank._create_sentence_graph(self.sentences, self.words)
        self.assertIsNotNone(self.textrank.graph)
        self.assertTrue(len(self.textrank.graph.vertices) == len(self.sentences))
        self.assertIsNotNone(self.textrank.graph.edges)
        self.assertTrue(len(self.textrank.graph.edges) > 0)

    def test_pagerank(self):
        self.textrank._create_sentence_graph(self.sentences, self.words)
        scores = self.textrank._pagerank()
        self.assertTrue(len(scores) == len(self.textrank.graph.vertices) == len(self.sentences))

    def test_process_results(self):
        self.textrank._create_sentence_graph(self.sentences, self.words)
        number_of_sentences = 1
        scores = self.textrank._pagerank()
        processed_scores = self.textrank._process_results(scores, number_of_sentences)
        self.assertIsNotNone(processed_scores)
        self.assertTrue(len(processed_scores) > 0)
        self.assertTrue(processed_scores == "Sentence 1", processed_scores)

    def test_execute(self):
        with open('../example/article.txt', 'r') as example:
            text = example.read()
        processed_score = self.textrank.execute(text, 1)
        expected_score = '''The President-elect's unusual call with Taiwan President Tsai Ing-wen on Friday led to a diplomatic protest, although Vice President-elect Mike Pence played down its significance, saying it was a "courtesy", not intended to show a shift in US policy on China.'''
        self.assertTrue(processed_score == expected_score, processed_score)
