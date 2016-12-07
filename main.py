from webcrawler.crawler import Crawler
from summarizer.summarize import summarize
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize text in file')
    parser.add_argument('file', help='name of file containing text to summarize')
    parser.add_argument('sentences', type=int, help='number of sentences in summary')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    crawler = Crawler(args.file)
    summary = summarize(text=crawler.get_content(), number_of_sentences=args.sentences)
    print(summary)
