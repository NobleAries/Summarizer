import unittest
from webcrawler.crawler import Crawler


class CrawlerTestCase(unittest.TestCase):
    def setUp(self):
        self.url = "/tests/data/main_page_test.html"
        self.crawler = Crawler(self.url)
        self.mainPage = '<a class="media__link" href="/news/world-us-canada-38564478"  rev="hero1|headline" >  Trump ' \
                        'prosecutor denies KKK sympathies  </a>' \
                        '<a class="media__link" href="http://www.bbc.co.uk/news/entertainment-arts-38570338" ' \
                        'rev="hero2|headline" > Tom Hiddleston sorry for Golden Globes speech </a> '
        self.inside = '<title>Kabul bombings: Dozens dead after twin blasts near Afghan parliament - BBC News</title>' \
                      '<div class="story-body__inner" property="articleBody">' \
                      '><p class="story-body__introduction">At least 30 people have been killed and 80 wounded in ' \
                      'twin bombings near the Afghan parliament in the capital Kabul.</p>' \
                      '<p>The blasts, part of a wave of attacks across Afghanistan on Tuesday, took place during rush ' \
                      'hour as staff were leaving the complex. </p>' \
                      '</div>'

    def test_process_article(self):
        art = self.crawler._process_articles(self.inside)
        self.assertEqual(art.title, 'Kabul bombings: Dozens dead after twin blasts near Afghan parliament - BBC News')
        self.assertEqual(art.text, 'At least 30 people have been killed and 80 wounded in twin bombings near the '
                                   'Afghan parliament in the capital Kabul. The blasts, part of a wave of attacks '
                                   'across Afghanistan on Tuesday, took place during rush hour as staff were leaving '
                                   'the complex. ')

unittest.main()