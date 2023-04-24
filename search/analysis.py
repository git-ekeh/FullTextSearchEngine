#!/usr/bin/env python3\

import re
import string
import Stemmer

STOPWORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in','that','have'
'I','it','for','not','on','with','he','as','you','do','at','this','but',
'his','by','from' ])

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

STEMMER = Stemmer.Stemmer('english')

def tokenize(text):
    return text.split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def stem_filter(tokens):
    return STEMMER.stemWords(tokens)

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]

def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]

def analyze(text):
    '''
    This function brings all these filters together
    It will tokenize the text into individual words
    then apply each filter in succession to the list
    of tokens
    '''
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]
