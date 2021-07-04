import urllib.parse
import urllib.request
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from typing import List

from bs4 import BeautifulSoup
from nltk import sent_tokenize
from readability import Document as Content
from ViNLP import word_tokenize

from ..text.document import Document
from ..text.sentence import Sentence


class SearchEngine:
    __instance = None
    __ignores = ['google.com', 'youtube.com']
    __link_per_page = 10
    __search_url = 'https://google.com/search?%s'

    def __init__(self):
        if SearchEngine.__instance is not None:
            return SearchEngine.__instance
        else:
            SearchEngine.__instance = self
            self.pool = Pool(cpu_count())

    def search(self, query: str) -> List[str]:
        num_pages = cpu_count()
        payloads = [urllib.parse.urlencode(
            {'q': query, 'start': i * self.__link_per_page}) for i in range(num_pages)]
        page_results = self.pool.map(self.search_per_page, payloads)
        results = [link for links in page_results for link in links]
        return results

    @classmethod
    def search_per_page(cls, params: dict) -> List[str]:
        req = urllib.request.Request(cls.__search_url % params,
                                     headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp.read().decode('utf-8'), 'lxml')
        anchors = soup.findAll('a')
        links = []
        for a in anchors:
            link = a.get('href')
            if link.startswith('/url?q=https') and not any(domain in link for domain in cls.__ignores):
                link = urllib.parse.urlparse(link, 'https')
                link = urllib.parse.parse_qs(link.query)['q'][0]
                links.append(link)
        return links

    @classmethod
    def get_content(cls, url: str) -> str:
        req = urllib.request.Request(url,
                                     headers={'User-Agent': 'Mozilla/5.0'})
        try:
            resp = urllib.request.urlopen(req)
        except:
            return None
        doc = Content(resp.read().decode('utf-8'))
        soup = BeautifulSoup(doc.summary(), "lxml")
        content = soup.get_text()
        paragraphs = [p for p in (content.splitlines()) if p != '']

        sents = []
        for paragraph in paragraphs:
            sents += sent_tokenize(paragraph)
        sents = [Sentence(sent) for sent in sents]
        return Document(sents)

    def get_all_contents(self, urls: List[str]) -> List[str]:
        contents = self.pool.map(self.get_content, urls)
        return [content for content in contents if content is not None]
