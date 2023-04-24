#!/usr/bin/env python3
import gzip
from lxml import etree
import time

from search.documents import Abstract

def load_documents():
    start = time.time()
    with open('corpus.xml','rb') as abstract:
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
