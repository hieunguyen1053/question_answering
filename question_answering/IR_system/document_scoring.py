import math
from typing import List

import numpy as np

from ..text.document import Document
from ..text.sentence import Sentence


class DocumentScoring:
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.N = len(self.documents)

    @property
    def words(self):
        words = set()
        for doc in self.documents:
            for word in doc.words:
                words.add(word)
        return words

    def tf(self, words: List[str], doc: Document):
        arr = np.zeros(len(words))
        for i, word in enumerate(words):
            arr[i] = math.log10(doc.count(word) + 1)
        return arr

    def df(self, words: List[str]):
        arr = np.zeros(len(words))
        for i, word in enumerate(words):
            arr[i] = sum([doc.has(word) for doc in self.documents])
        return arr

    def idf(self, word: str):
        return np.log10(self.N / self.df(word))

    def tf_idf(self, word: str, doc: Document):
        return self.tf(word, doc) * self.idf(word)

    def score(self, query: List[str], doc: Document):
        dis = np.linalg.norm(self.tf_idf(self.words, doc))
        return np.sum(self.tf_idf(query, doc) / dis)

    def ranking(self, query: List[str]):
        docs_rank = {}
        for doc in self.documents:
            docs_rank[doc] = self.score(query, doc)
        documents = sorted(self.documents, key=lambda x: docs_rank[x], reverse=True)
        documents = filter(lambda doc: docs_rank[doc] > 0, documents)
        return documents


if __name__ == '__main__':
    documents = [
        Document(Sentence('Sweet sweet nurse Love')),
        Document(Sentence('Sweet sorrow')),
        Document(Sentence('How sweet is love')),
        Document(Sentence('Nurse')),
    ]
    system = DocumentScoring(documents)
    # print(system.score(['sweet', 'love'], system.documents[0]))
    print(system.tf(['love', 'sweet', 'sorrow',
          'how', 'nurse', 'is'], documents[0]))
    print(system.df(['love', 'sweet', 'sorrow', 'how', 'nurse', 'is']))
    print(system.idf(['love', 'sweet', 'sorrow', 'how', 'nurse', 'is']))
    print(system.tf_idf(['love', 'sweet', 'sorrow',
          'how', 'nurse', 'is'], documents[0]))
    print(system.score(['sweet', 'love'], documents[0]))
