#!/usr/bin/env python3

from collections import Counter
from dataclasses import dataclass

from .analysis import analyze


@dataclass

class Abstract:
    '''Amazon Policy text'''
    ID: int
    title: str
    abstract: str

    @property    #concatenates the title and the contents of the abstract, we are only interested in the contents of the abstract anyways
    def fulltext(self):
        return ' '.join([self.title, self.abstract])

    def analyze(self):
        self.term_frequencies = Counter(analyze(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term,0)
