#!/usr/bin/env python3
from collections import Counter
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import io
#from .analysis import analyze
import time
from lxml import etree
import Stemmer
import re
import string
import os.path
import requests
#from search.documnets import Abstract

@dataclass #this data class is a convenient way to access the data we want
class Abstract:
    '''Amazon Policy text'''
    ID: int
    title: str
    abstract: str

    @property    #concatenates the title and the contents of the abstract, we are only interested in the contents of the abstract anyways
    def fulltext(self):
        return ' '.join([self.title, self.abstract])

    #def analyze(self):
        #self.term_frequencies = Counter(analyze(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term,0)

'''
READ THIS DO NOT SKIP

We will want to extract the abstracts from the XML and parse them so we can create
instances of our Abstract object. We will assign each document an ID in order of
loading (i.e. the first document will have ID=1, the second will have ID=2, and so on)
'''

def load_documents():
    start = time.time()
    with open('amazon_stokens.xml','rb') as abstract:
        doc_id = 1
            # iterparse will yield the entire doc element once it finds the
            # closing '</doc>' tag
        for _, element in etree.iterparse(abstract, events=('end',), tag='doc'):
            title = element.findtext('./title')
            abstract = element.findtext('./abstract')

            yield Abstract(ID=doc_id, title=title, abstract=abstract)

            doc_id += 1
                # the element.clear() call will explicitly free up the memory
                # used to store the element
                #element.clear()

        end = time.time()
        print(f'Parsing XML took' + str((end - start)) +  'seconds')

#with open('amazon_stokens.xml', 'rb') as abstract:
#open_file = open('amazon_stokens.xml', 'r')
#amazon_stokens = open_file.read()
#saved_file = amazon_stokens.close()
    #parser = ET.XMLParser(encoding='utf-8')
    #tree = ET.parse(amazon_stokens, parser = parser)
    #root = tree.getroot()


'''
READ THIS DO NOT SKIP

We are going to store this in a data structure known as an "inverted index"
or a posting list. Think of it as the index in the back of a book that has an alphabetized
list of relevant words and concepts, and on what page number a reader can find them

Practically, what this means is that we are going to create a dictionary where
we map all the words in our corpus to the IDs of the documents they occur in.

*** This is where you need to map each sentence to the document it is in or the meta-data groups it is in ***

When developing ETL pipeline combine all steps used in each step into one object
and apply that object to rest of the text

The index will have to take loaded

The analyze function returns the tokens that is all it is useful for
Might as well just return the data in a tokenized manner
'''

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



class Index:
    '''
    The Index class that will store the index and the documents
    The documents dictionary stores the dataclasses by ID, and
    the index keys will be the tokens, with the values being the
    document IDs the token occurs in
    '''
    def __init__(self):
        self.index = {}
        self.documents = {}

    def index_document(self, document):
        if document.ID not in self.documents:
            self.documents[document.ID] = document

        for token in analyze(document.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.ID)
    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]

    def search(self, query):
        '''
        Boolean search; this will return documents that contain all words from the query,
        but not rank them (sets are fast, but unordered)
        '''

        analyzed_query = analyze(query)
        results = self._results(analyzed_query)
        documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]

        return documents




'''
SEARCHING

Now we have all tokens indexed, searching for a query becomes a matter of
analyzing the query text with the same analyzer as we applied to the documents;
this way we'll end up with tokens that should match the tokens in the index.

For each token, we'll do a lookup in the dictionary, finding the document IDs that
the token occurs in. We do this for every token, and then find the IDs of documents
in all these sets (i.e. for a document to match the query, it needs to contain all
the tokens in the query).

We will then take the resulting list of document IDs, and fetch the actual data from our
documents store
'''


index.search('Privacy Policy: Amazon')
