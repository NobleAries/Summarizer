from bs4 import BeautifulSoup
import requests
import re


class Crawler(object):
    def __init__(self, url):
        self.url = url

    # kind of works for http://bbc.com/:
    def get_content(self):

        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")

        classes_with_links = soup.find_all('a', {'class': 'media__link'}, href=True)

        articles = []

        pattern = re.compile("^https?://")

        for link in classes_with_links:
            if pattern.match(link.get('href')):
                art_r = requests.get(link.get('href'))
                article_soup = BeautifulSoup(art_r.text, "lxml")
                article_text = article_soup.find('div', {'property': 'articleBody'})
                if article_text is not None:
                    for at in article_text.find_all('p'):
                        if at is not None:
                            print(at.text)
                            articles.append(at.text)
            else:
                absolute_link = self.url + link.get('href')
                art_r = requests.get(absolute_link)
                article_soup = BeautifulSoup(art_r.text, "lxml")
                article_text = article_soup.find('div', {'property': 'articleBody'})
                if article_text is not None:
                    for at in article_text.find_all('p'):
                        if at is not None:
                            print(at.text)
                            articles.append(at.text)

        return articles
