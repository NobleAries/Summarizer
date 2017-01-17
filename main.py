from webcrawler.crawler import Crawler
from summarizer.summarize import Summarizer
from summarizer.textrank import TextRankAlgorithm
from summarizer.sumbasic import SumBasicAlgorithm
from summarizer.tf_idf import TfIdfCalculator
from summarizer.words_frequencies_graph import WordsFrequenciesGraph
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize articles from given url')
    parser.add_argument('url', help='url to get articles from')
    parser.add_argument('--sentences', type=int, help='number of sentences in summary', default=3)
    parser.add_argument('--outfile', help='name of file to store result of summarization', default=None)
    parser.add_argument('--algorithm', help='which algorithm to use', choices=['textrank', 'sumbasic'],
                        default='textrank')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    crawler = Crawler(args.url)
    algorithm_dict = {'textrank': TextRankAlgorithm(), 'sumbasic': SumBasicAlgorithm()}
    algorithm = algorithm_dict[args.algorithm]
    summarizer = Summarizer(algorithm)

    print('Fetching articles...')
    articles = crawler.get_content()

    print('Computing tf-idf...')
    tf_idf_calc = TfIdfCalculator([article.text for article in articles])
    tf_idf_calc.choose_best_words(number=5)

    print('Drawing frequencies graph')
    freq_graph = WordsFrequenciesGraph([article.text for article in articles])
    freq_graph.draw_graph()

    for article in articles:
        print('Summarizing article: ', article.title)
        summary = summarizer.summarize(text=article.text, number_of_sentences=args.sentences, output_file=args.outfile,
                                       title=article.title)
        print(summary)
        print()

