from typing import List, Union

from ViNLP import word_tokenize


class Sentence:
    def __init__(self, words: Union[List[str], str]):
        if isinstance(words, str):
            self.words = word_tokenize(words)
        else:
            self.words = words

        self.words = [word.lower() for word in self.words]

    def count(self, word: str):
        return self.words.count(word)

    def has(self, word: str):
        return self.count(word) > 0