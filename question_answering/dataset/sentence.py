from collections import Counter
from typing import List, Union

from ViNLP import word_tokenize

from .stopwords import STOPWORDS


class Sentence:
    def __init__(self, words: Union[List[str], str]):
        if isinstance(words, str):
            self.words = word_tokenize(words)
        else:
            self.words = words

    @property
    def unique_words(self):
        return set([word.lower() for word in self.words])

    def to_str(self):
        return ' '.join(self.words)

    def __str__(self) -> str:
        return self.to_str()