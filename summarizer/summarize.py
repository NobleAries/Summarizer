from abc import ABCMeta, abstractmethod


class SummarizationAlgorithm(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, text, number_of_sentences):
        pass


class Summarizer:

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def summarize(self, text, number_of_sentences, output_file=None):
        summary = self.algorithm.execute(text, number_of_sentences)
        if output_file:
            with open(output_file, 'a') as file:
                file.write(summary + '\n\n')
        return summary
