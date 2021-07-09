from typing import List, Union
from .sentence import Sentence

class Document:
    def __init__(self, sentences: Union[List[Sentence], Sentence]):
        if isinstance(sentences, Sentence):
            self.sentences = [sentences]
        else:
            self.sentences = sentences

    @property
    def unique_words(self):
        sentences = self.sentences
        unique_words = sentences[0].unique_words
        for i in range(1, len(sentences)):
            unique_words |= sentences[i].unique_words
        return unique_words

    def to_str(self) -> str:
        return ' '.join([sent.to_str() for sent in self.sentences])

    def __str__(self) -> str:
        return self.to_str()