import nltk
import string


class NaturalLanguageProcessor:

    @staticmethod
    def split_by_sentences(text):
        return nltk.sent_tokenize(text)

    @staticmethod
    def split_by_words(sentence):
        words = nltk.word_tokenize(sentence)
        return NaturalLanguageProcessor._process_words(words)

    @staticmethod
    def _process_words(words):
        with open('summarizer\stopwords.txt', 'r') as file:
            stop_words = file.read().split('\n')
        words = NaturalLanguageProcessor.remove_punctuation(words)
        words = NaturalLanguageProcessor.remove_stop_words(words, stop_words)
        words = NaturalLanguageProcessor.remove_empty_strings(words)
        return words

    @staticmethod
    def remove_stop_words(words_to_filter, stop_words):
        def lowercase_first_letter(word):
            return word[0].lower() + word[1:] if word else ''

        return list(filter(lambda word: lowercase_first_letter(word) not in stop_words, words_to_filter))

    @staticmethod
    def remove_punctuation(words):
        return list(map(lambda word: word.strip(string.punctuation), words))

    @staticmethod
    def remove_empty_strings(words):
        return list(filter(lambda word: word, words))
