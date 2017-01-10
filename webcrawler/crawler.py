from bs4 import BeautifulSoup
import requests
import re
import threading


class Article:
    def __init__(self, title, text):
        self.title = title
        self.text = text


class Crawler(object):
    def __init__(self, url):
        self.url = url
        self._found_links = []
        self.articles = []
        self._links_lock = threading.Lock()
        self._articles_lock = threading.Lock()

    def _process_articles(self, link):
        art_r = requests.get(link)
        article_soup = BeautifulSoup(art_r.text, "lxml")
        article_title = article_soup.find('title')
        article_text = article_soup.find('div', {'property': 'articleBody'})
        if article_text:
            txt = []
            for at in article_text.find_all('p'):
                if at:
                    txt.append(at.text)
            return Article(article_title.text, " ".join(txt))

    def _process_links(self):

        pattern = re.compile("^https?://")
        self._links_lock.acquire()
        while self._found_links:
            link = self._found_links.pop()
            self._links_lock.release()
            absolute_link = link.get('href') if pattern.match(link.get('href')) else self.url + link.get('href')
            article = self._process_articles(absolute_link)
            if article:
                self._articles_lock.acquire()
                self.articles.append(article)
                self._articles_lock.release()

            self._links_lock.acquire()
        self._links_lock.release()



    # kind of works for http://bbc.com/:
    def get_content(self):

        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")
        self._found_links = soup.find_all('a', {'class': 'media__link'}, href=True)
        threads = []
        for i in range(0, 6):
            threads.append(threading.Thread(target=self._process_links))
            threads[i].start()

        for t in threads:
            t.join()

        return self.articles




