import unittest

import itertools

from summarizer.sumbasic import SumBasicAlgorithm
from summarizer.nlp import NaturalLanguageProcessor


class TextRankTestCase(unittest.TestCase):
    def setUp(self):
        self.sumbasic = SumBasicAlgorithm()
        self.text = (
            'Test1. Test2. Test2 Test3.')
        self.sentences = NaturalLanguageProcessor.split_by_sentences(self.text)
        self.words_in_sentence = {sentence: NaturalLanguageProcessor.split_by_words(sentence) for sentence in
                                  self.sentences}
        self.all_words = list(
            itertools.chain.from_iterable(self.words_in_sentence.values()))  # list of words from all sentences

    def test_compute_words_probabilities(self):
        self.sumbasic._compute_words_probabilities(self.all_words)
        self.assertEqual(self.sumbasic.word_probability["Test2"], 0.5, self.sumbasic.word_probability["Test2"])
        self.assertEqual(self.sumbasic.word_probability["Test1"], 0.25, self.sumbasic.word_probability["Test1"])
        self.assertEqual(self.sumbasic.word_probability["Test3"], 0.25, self.sumbasic.word_probability["Test3"])

    def test_compute_sentence_weight(self):
        self.sumbasic._compute_words_probabilities(self.all_words)
        sentence_weight_dict = {
            sentence: self.sumbasic._compute_sentence_weight(self.words_in_sentence[sentence], len(sentence))
            for sentence in self.sentences}
        self.assertEqual(len(self.sentences), len(sentence_weight_dict), len(sentence_weight_dict))

    def test_update_word_probabilities(self):
        self.sumbasic._compute_words_probabilities(self.all_words)
        self.assertEqual(self.sumbasic.word_probability["Test2"], 0.5, self.sumbasic.word_probability["Test2"])
        self.sumbasic._update_word_probabilities(self.words_in_sentence['Test2.'])
        self.assertEqual(self.sumbasic.word_probability["Test2"], 0.25, self.sumbasic.word_probability["Test2"])

    def test_choose_best_sentence(self):
        self.sumbasic._compute_words_probabilities(self.all_words)
        sentence_weight_dict = {
            sentence: self.sumbasic._compute_sentence_weight(self.words_in_sentence[sentence], len(sentence))
            for sentence in self.sentences}
        best_sentence = self.sumbasic._choose_best_sentence(sentence_weight_dict)
        self.assertEqual(best_sentence, "Test2.")

    def test_execute(self):
        result = self.sumbasic.execute(self.text, 1)
        self.assertIsNotNone(result)
        self.assertEqual("Test2.", result)
