from .nlp import NaturalLanguageProcessor as nlp
import math
import operator


class TfIdfCalculator:

    def __init__(self, documents):
        self.documents = documents
        self.words_in_documents = [nlp.split_by_words(document) for document in self.documents]

    @staticmethod
    def tf(term, words_in_document):
        return words_in_document.count(term)

    def idf(self, term):
        documents_containing_term = 0
        for words_in_document in self.words_in_documents:
            if term in words_in_document:
                documents_containing_term += 1
        return math.log10(len(self.documents) / (1 + documents_containing_term))

    def tf_idf(self, term, words_in_document):
        tf = self.tf(term, words_in_document)
        idf = self.idf(term)
        return tf * idf

    def choose_best_words(self, number=5):
        for document, words_in_document in zip(self.documents, self.words_in_documents):
            tf_idf_values = [(term, self.tf_idf(term, words_in_document)) for term in set(words_in_document)]
            tf_idf_values.sort(key=operator.itemgetter(1), reverse=True)
            self.print_results(document, tf_idf_values[:number])

    @staticmethod
    def print_results(document, tf_idf_values):
        print(document)
        for term, tf_idf_value in tf_idf_values:
            print(term, ': ', tf_idf_value)
