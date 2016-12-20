import nltk


class NaturalLanguageProcessor:

    @staticmethod
    def split_by_sentences(text):
        return nltk.sent_tokenize(text)

    @staticmethod
    def split_by_words(sentence):
        return nltk.word_tokenize(sentence)