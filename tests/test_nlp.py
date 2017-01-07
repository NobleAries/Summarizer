import unittest
import os
from summarizer.nlp import NaturalLanguageProcessor


class NaturalLanguageProcessorTestCase(unittest.TestCase):

    def setUp(self):
        self.text = "First sentence. Sentence second, sentence third. Let us summarize text for you."
        self.sentence = "I want to believe in ghosts,    they are scary though."
        self.words = [",", "I", "Him", "Sample", "-", "word", ".", " ", ""]

    def test_split_by_sentences(self):
        sentences = NaturalLanguageProcessor.split_by_sentences(self.text)
        self.assertTrue(len(sentences), 3)
        self.assertEqual(sentences[0], "First sentence.")
        self.assertEqual(sentences[1], "Sentence second, sentence third.")
        self.assertEqual(sentences[2], "Let us summarize text for you.")

    def test_split_by_words(self):
        words = NaturalLanguageProcessor.split_by_words(self.sentence)
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0], "ghosts")
        self.assertEqual(words[1], "scary")

    def test_process_words(self):
        words = NaturalLanguageProcessor._process_words(self.words)
        self.assertEqual(len(words), 3)
        self.assertEqual(words[0], "Sample")
        self.assertEqual(words[1], "word")
        self.assertEqual(words[2], " ")

    def test_remove_stop_words(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'summarizer', 'stopwords.txt'), 'r') as file:
            stop_words = file.read().split('\n')
        words = NaturalLanguageProcessor.remove_stop_words(self.words, stop_words)
        self.assertEqual(len(words), 7)
        self.assertEqual(words[0], ",")
        self.assertEqual(words[1], "Sample")
        self.assertEqual(words[2], "-")
        self.assertEqual(words[3], "word")
        self.assertEqual(words[4], ".")
        self.assertEqual(words[5], " ")
        self.assertEqual(words[6], "")

    def test_remove_punctuation(self):
        words = NaturalLanguageProcessor.remove_punctuation(self.words)
        self.assertEqual(len(words), 9)
        self.assertEqual(words[0], "")
        self.assertEqual(words[1], "I")
        self.assertEqual(words[2], "Him")
        self.assertEqual(words[3], "Sample")
        self.assertEqual(words[4], "")
        self.assertEqual(words[5], "word")
        self.assertEqual(words[6], "")
        self.assertEqual(words[7], " ")
        self.assertEqual(words[8], "")

    def test_remove_empty_strings(self):
        words = NaturalLanguageProcessor.remove_empty_strings(self.words)
        self.assertEqual(len(words), 8)
        self.assertEqual(words[0], ",")
        self.assertEqual(words[1], "I")
        self.assertEqual(words[2], "Him")
        self.assertEqual(words[3], "Sample")
        self.assertEqual(words[4], "-")
        self.assertEqual(words[5], "word")
        self.assertEqual(words[6], ".")
        self.assertEqual(words[7], " ")
