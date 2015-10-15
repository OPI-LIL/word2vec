import string
import xml.etree.cElementTree as ET
from string import digits

from nltk.tokenize import sent_tokenize, word_tokenize

from mixins import  LogMixin


class NKJPSentences(object, LogMixin):
    def __init__(self, rootPath, fileName, limit=None):
        self.rootPath = rootPath
        self.fileName = fileName
        self.limit = limit

    def __iter__(self):
        from itertools import islice

        sentences = self.fetch(self.rootPath, self.fileName)

        if self.limit is not None:
            sentences = islice(sentences, self.limit)

        for sentence in sentences:
            yield sentence

    def xml_to_wordlist(self, filePath):
        tree = ET.parse(filePath)
        root = tree.getroot()

        for element in root.iter("{http://www.tei-c.org/ns/1.0}ab"):

            # Tokenize to sentences
            for sentence in sent_tokenize(element.text):
                # Remove digits and punctuation
                clean_sentence = sentence.encode('utf-8', 'ignore').translate(None, string.punctuation + digits)

                # Tokenize words
                yield word_tokenize(clean_sentence)

    def fetch(self, rootPath, fileName):
        import os
        from os.path import join

        for root, dirs, files in os.walk(rootPath):
            if fileName in set(files):
                for word in self.xml_to_wordlist(join(root, fileName)):
                    yield word