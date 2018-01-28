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
        if re.findall(r'->', file_handler.read()):
            raise IOError("Containing unsupported symbol '->'")
            sys.exit(1)

        file_handler.seek(0)
        for item in Stemmer.stem(file_handler):
            print(item)

        # data pre-processing step 1: trim grammar
        file_handler.seek(0)
        file_content = file_handler.read()
        file_content = re.sub(r'\#.*', '', file_content)
        file_content = re.sub(r'(""")\s*.*\s*\1', '', file_content)
        file_content = re.sub(r"(''')\s*.*\s*\1", '', file_content)

        # data pre-processing step 2: fetch the sentence
        grammar = Grammar.from_file(file_content)
        sentence = Sentence.from_file(file_content, grammar)
        grammar.trim_terminal_rules()
        return (grammar, sentence)

def run():
    try:
        # either get the file name from -f option or standard input
        parser = OptionParser()
        parser.add_option("-f", "--file", action="store", dest="filename", help="indicate the file name", metavar="FILE")
        options, _ = parser.parse_args()

        if options.filename:
            grammar, sentence = MyEarleyParserFileReader.readfile(options.filename)
        else:
            print('Please input the file name: ')
            lines = sys.stdin.readlines()
            if lines is None or len(lines) == 0:
                raise IOError('Missing content from standard input')
                sys.exit(1)

            # create an intermediate file for future reference
            filename = "intermediate.dat"
            file_handler = open(filename, 'w')
            file_handler.writelines(lines)
            file_handler.close()

            grammar, sentence = MyEarleyParserFileReader.readfile(filename)
    except IOError as err:
        print("IO error: {0}".format(err))
        sys.exit(1)
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(1)
    except:
        """handle generic errors"""
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
