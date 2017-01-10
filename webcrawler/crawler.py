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
        self.found_links = []
        self.articles = []
        self.links_lock = threading.Lock()
        self.articles_lock = threading.Lock()

    def process_links(self):

        pattern = re.compile("^https?://")
        self.links_lock.acquire()
        while self.found_links:
            link = self.found_links.pop()
            self.links_lock.release()

            absolute_link = link.get('href') if pattern.match(link.get('href')) else self.url + link.get('href')

            art_r = requests.get(absolute_link)
            article_soup = BeautifulSoup(art_r.text, "lxml")
            article_title = article_soup.find('title')
            article_text = article_soup.find('div', {'property': 'articleBody'})
            if article_text:
                txt = []
                for at in article_text.find_all('p'):
                    if at:
                        txt.append(at.text)
                article = Article(article_title.text, " ".join(txt))
                self.articles_lock.acquire()
                self.articles.append(article)
                self.articles_lock.release()

            self.links_lock.acquire()
        self.links_lock.release()



    # kind of works for http://bbc.com/:
    def get_content(self):

        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")

        self.found_links = soup.find_all('a', {'class': 'media__link'}, href=True)

        threads = []
        for i in range(0, 6):
            threads.append(threading.Thread(target=self.process_links))
            threads[i].start()

        for t in threads:
            t.join()

        return self.articles




