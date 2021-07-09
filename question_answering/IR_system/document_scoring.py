from string import punctuation
from typing import List

import numpy as np
from ..dataset.document import Document
from ..dataset.sentence import Sentence
from ..dataset.stopwords import STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer


def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class DocumentScoring:
    def __init__(self, documents: List[Document], query: str):
        self.documents = documents
        self.query = query

        self.vectorizer = TfidfVectorizer(stop_words=set(STOPWORDS) | set(punctuation))

    def tf_idf(self):
        documents = list(map(lambda doc: doc.to_str(), self.documents))
        query = Sentence(self.query).to_str()
        return self.vectorizer.fit_transform([query] + documents).A

    def score(self):
        matrix = self.tf_idf()
        query = matrix[0, :]
        documents = matrix[1:, :]

        score = np.zeros(documents.shape[0])
        for i, doc in enumerate(documents):
            score[i] = cos_sim(query, doc)
        return score

    def rank(self):
        score = self.score()
        return np.argsort(-score)

    def sorted_documents(self):
        rank = self.rank()
        documents = []
        for idx in range(len(self.documents)):
            documents.append(self.documents[rank[idx]])
        return documents

class PassageScoring:
    def __init__(self, document: Document, query: str):
        self.sentences = document.sentences
        self.query = query

        self.vectorizer = TfidfVectorizer(stop_words=set(STOPWORDS) | set(punctuation))

    def tf_idf(self):
        sentences = list(map(lambda sent: sent.to_str(), self.sentences))
        query = Sentence(self.query).to_str()
        return self.vectorizer.fit_transform([query] + sentences).A

    def score(self):
        matrix = self.tf_idf()
        query = matrix[0, :]
        sentences = matrix[1:, :]

        score = np.zeros(sentences.shape[0])
        for i, doc in enumerate(sentences):
            score[i] = cos_sim(query, doc)
        return score

    def rank(self):
        score = self.score()
        return np.argsort(-score)

    def filterd_passage(self, threshold=0.1):
        rank = self.rank()
        sentences = []
        for idx in range(len(self.sentences)):
            sentences.append(self.sentences[rank[idx]])
        return Document(sentences)
