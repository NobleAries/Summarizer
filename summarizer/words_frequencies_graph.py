from .nlp import NaturalLanguageProcessor as nlp
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import itertools


class WordsFrequenciesGraph:
    def __init__(self, documents):
        self.documents = documents
        self.words_in_documents = [nlp.split_by_words(document) for document in self.documents]

    def count_words(self):
        all_words = list(itertools.chain.from_iterable(self.words_in_documents))
        print(all_words)
        freq_distribution = Counter(all_words)
        print(freq_distribution)
        return freq_distribution.most_common(100)

    def draw_graph(self):
        labels, values = zip(*self.count_words())
        indexes = np.arange(len(labels))
        width = 1
        plt.bar(indexes, values, width, color='green', alpha=0.4)
        plt.xticks(indexes + width * 0.5, labels, rotation=90)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Words Frequencies Graph')
        plt.legend()
        plt.show()
