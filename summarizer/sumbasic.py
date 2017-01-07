from .summarize import SummarizationAlgorithm
from .nlp import NaturalLanguageProcessor
import itertools
from collections import Counter


class SumBasicAlgorithm(SummarizationAlgorithm):

    def execute(self, text, number_of_sentences):
        sentences = NaturalLanguageProcessor.split_by_sentences(text)
        if number_of_sentences > len(sentences):
            number_of_sentences = len(sentences)
        words_in_sentence = {sentence: NaturalLanguageProcessor.split_by_words(sentence) for sentence in sentences}
        all_words = list(itertools.chain.from_iterable(words_in_sentence.values()))  # list of words from all sentences
        self._compute_words_probabilities(all_words)

        sentences_in_summary = set()
        while len(sentences_in_summary) < number_of_sentences:
            sentence_weight_dict = {sentence: self._compute_sentence_weight(words_in_sentence[sentence], len(sentence))
                                    for sentence in sentences}
            best_sentence = self._choose_best_sentence(sentence_weight_dict)
            sentences_in_summary.add(best_sentence)
            self._update_word_probabilities(words_in_sentence[best_sentence])

        return '\n'.join(sentences_in_summary)

    def _compute_words_probabilities(self, words):
        counter = Counter()
        for word in words:
            counter[word] += 1
        self.word_probability = dict(counter)
        for key, value in self.word_probability.items():
            self.word_probability[key] = value / len(words)

    def _compute_sentence_weight(self, words_in_sentence, sentence_length):
        weight = 0
        for word in words_in_sentence:
            weight += self.word_probability[word] / sentence_length
        return weight

    @staticmethod
    def _choose_best_sentence(sentence_weight_dict):
        return max(sentence_weight_dict.keys(), key=lambda sentence: sentence_weight_dict[sentence])

    def _update_word_probabilities(self, words_to_update):
        for word in words_to_update:
            self.word_probability[word] *= self.word_probability[word]