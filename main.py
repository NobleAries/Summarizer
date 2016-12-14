from webcrawler.crawler import Crawler
from summarizer.summarize import summarize
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize text in file')
    parser.add_argument('infile', help='name of file containing text to summarize')
    parser.add_argument('--sentences', type=int, help='number of sentences in summary', default=3)
    parser.add_argument('--outfile', help='name of file to store result of summarization', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    crawler = Crawler(args.infile)
    summary = summarize(text=crawler.get_content(), number_of_sentences=args.sentences, outfile=args.outfile)
    print(summary)
