import unittest

from summarizer.textrank import TextRankAlgorithm
from summarizer.graphutils.graph import Graph
from summarizer.nlp import NaturalLanguageProcessor


class TextRankTestCase(unittest.TestCase):
    def setUp(self):
        self.textrank = TextRankAlgorithm()
        self.sentences = ["Sentence 1", "Sentence 1", "Sentence 2", "Sentence 3"]
        self.words = {sentence: NaturalLanguageProcessor.split_by_words(sentence) for sentence in self.sentences}

    def test_prepare_sentences_and_words(self):
        text = 'I don\'t think so. Donald Trump is the President of USA. Today, tomorrow or yesterday?' \
               'That is the very important question. Go study.'
        sentences, words = self.textrank._prepare_sentences_and_words(text)
        self.assertTrue(len(sentences) == 3)
        self.assertFalse('I don\'t think so' in sentences)
        self.assertFalse('Go study.' in sentences)
        self.assertTrue(len(words.keys()) == 3)
        self.assertTrue(words['That is the very important question.'] == ['important', 'question'])
        self.assertTrue(words['Donald Trump is the President of USA.'] == ['Donald', 'Trump', 'President', 'USA'])
        self.assertTrue(words['Today, tomorrow or yesterday?'] == ['Today', 'tomorrow', 'yesterday'])

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
        text = ('Donald Trump has complained about Chinese economic and military policy after a phone conversation with '
               'Taiwan\'s President drew the ire of Beijing. The President-elect\'s unusual call with Taiwan President '
               'Tsai Ing-wen on Friday led to a diplomatic protest, although Vice President-elect Mike Pence played '
               'down its significance, saying it was a "courtesy", not intended to show a shift in US policy on China. '
               '"Did China ask us if it was OK to devalue their currency (making it hard for our companies to '
               'compete), heavily tax our products going into their country (the U.S. doesn\'t tax them) or to build a '
               'massive military complex in the middle of the South China Sea? I don\'t think so!" Mr Trump said on '
               'Twitter. China, Taiwan, the Philippines, Vietnam, Malaysia and Brunei claim ownership of parts or '
               'all of the energy-rich South China Sea, through which trillions of dollars in trade passes '
               'annually.')
        processed_score = self.textrank.execute(text, 1)
        expected_score = ('The President-elect\'s unusual call with Taiwan President Tsai Ing-wen on Friday led to a '
                         'diplomatic protest, although Vice President-elect Mike Pence played down its significance, '
                         'saying it was a "courtesy", not intended to show a shift in US policy on China.')
        self.assertTrue(processed_score == expected_score, processed_score)
