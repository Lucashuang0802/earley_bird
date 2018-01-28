#!/usr/bin/python3
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys
import re
from sentence import *
from parser import *
from optparse import OptionParser
import traceback
from stemmer import *

class MyEarleyParserFileReader:
    @staticmethod
    def readfile(filename):
        file_handler = open(filename, 'r')
        for item in Stemmer.stem(file_handler):
            print(item)

        file_handler.seek(0)
        file_content = file_handler.read()
        file_content = re.sub(r'\#.*', '', file_content)
        file_content = re.sub(r'(""")\s*.*\s*\1', '', file_content)
        file_content = re.sub(r"(''')\s*.*\s*\1", '', file_content)

        # data pre-processing step 1: trim grammar and fetch the sentence
        grammar = Grammar.from_file(file_content)
        sentence = Sentence.from_file(file_content, grammar)
        grammar.trim_terminal_rules()
        return (grammar, sentence)

def run():

    # load grammar from file
    try:
        # provide option command line argument
        parser = OptionParser()
        parser.add_option("-f", "--file", action="store", dest="filename", help="indicate the file name", metavar="FILE")
        options, _ = parser.parse_args()

        # either get the file name from -f option or standard input
        filename = None
        if options.filename:
            filename = options.filename
        else:
            filename = input('Please input the file name: ')
        grammar, sentence = MyEarleyParserFileReader.readfile(filename)
    except IOError as err:
        print("IO error: {0}".format(err))
        sys.exit(1)
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(1)
    except:
        print("Unexcept error: {0}".format(sys.exc_info()))
        traceback.print_exc()
        sys.exit(1)

    # run parser
    earley = Parser(grammar, sentence)
    earley.parse()

    # output sentence validity
    if earley.is_valid_sentence():
        print('==> Sentence is valid.')
    else:
        print('==> Sentence is invalid.')

if __name__ == '__main__':
    run()
