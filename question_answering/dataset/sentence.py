from collections import Counter
from typing import List, Union

from ViNLP import word_tokenize
from .stopwords import STOPWORDS

class Sentence:
    def __init__(self, words: Union[List[str], str]):
        if isinstance(words, str):
            self._words = word_tokenize(words)
        else:
            self._words = words

        self.words = [word.lower() for word in self._words if word not in STOPWORDS]
        self.word_counter = Counter(self.words)

    def count(self, word: str):
        return self.word_counter[word]

    def has(self, word: str):
        return self.count(word) > 0

    def __str__(self) -> str:
        return ' '.join(self._words)