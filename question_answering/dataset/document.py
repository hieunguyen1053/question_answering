from typing import List, Union
from .sentence import Sentence

class Document:
    def __init__(self, sentences: Union[List[Sentence], Sentence]):
        if isinstance(sentences, Sentence):
            self.sentences = [sentences]
        else:
            self.sentences = sentences

    @property
    def words(self) -> List[str]:
        words = set()
        for sentence in self.sentences:
            for word in sentence.words:
                words.add(word)
        return words

    def count(self, word: str) -> int:
        return sum(sent.count(word) for sent in self.sentences)

    def has(self, word: str) -> bool:
        return self.count(word) > 0

    def __str__(self) -> str:
        return ' '.join([sent.__str__() for sent in self.sentences])