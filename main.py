from webcrawler.crawler import Crawler
from summarizer.summarize import Summarizer
from summarizer.textrank import TextRankAlgorithm
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize articles from given url')
    parser.add_argument('url', help='url to get articles from')
    parser.add_argument('--sentences', type=int, help='number of sentences in summary', default=3)
    parser.add_argument('--outfile', help='name of file to store result of summarization', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    crawler = Crawler(args.url)
    algorithm = TextRankAlgorithm()
    summarizer = Summarizer(algorithm)
    for article in crawler.get_content():
        summary = summarizer.summarize(text=article, number_of_sentences=args.sentences, output_file=args.outfile)
        print(summary)
        print()
