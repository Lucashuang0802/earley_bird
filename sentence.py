#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-
import re
import sys
from nltk.stem.porter import *

class Word:
    def __init__(self, word = '', tags = []):
        '''Initialize a word with a list of tags'''
        self.word = word
        self.tags = tags

    def __str__(self):
        '''Nice string representation'''
        return "{0}<{1}>".format(self.word, ','.join(self.tags))

class Sentence:
    def __init__(self, words = []):
        '''A sentence is a list of words'''
        self.words = words

    def __str__(self):
        '''Nice string representation'''
        return ' '.join(str(w) for w in self.words)

    def __len__(self):
        '''Sentence's length'''
        return len(self.words)

    def __getitem__(self, index):
        '''Return a word of a given index'''
        if index >= 0 and index < len(self):
            return self.words[index]
        else:
            return None

    def add_word(self, word):
        '''Add word to sentence'''
        self.words.append(word)

    @staticmethod
    def from_file(content, grammar):
        '''Create a Sentence object from a given string in the Apertium
           stream format:
              time/time<N> flies/flies<N>/flies<V> like/like<P>/like<V>
              an/an<D> arrow/arrow<N>'''
        sentence_finder = re.search('W\s*=\s*([a-zA-Z -]*)\.$', content)
        if sentence_finder is None:
            print("Possibly missing the sentence to parse")
            sys.exit()
        sentence = sentence_finder.group(1).strip()   
        words = sentence.split(' ')
        stemmer = PorterStemmer()
        sentence = Sentence()

        for word in words:
            tags = []
            for key in grammar.rules:
                rules = grammar[key]
                for rule in rules:
                    if stemmer.stem(word) in rule.rhs:
                        tags.append(key)
            sentence.add_word(Word(word, tags))
        return sentence
    