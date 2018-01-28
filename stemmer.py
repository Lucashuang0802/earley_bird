import sys
import string
from nltk.stem.porter import *

class Stemmer:
    @staticmethod
    def stem(file_reader):

        def isfloat(value):
            """Return if the value, which is a string, represents a float number in literal meaning"""
            try:
                _ = float(value)
            except ValueError:
                return False
            else:
                return True

        def isint(value):
            """Return if the value, which is a string, represents a integer number in literal meaning"""
            try:
                trial_float = float(value)
                trial_int = int(value)
            except ValueError:
                return False
            else:
                return trial_float == trial_int

        """This is a stemmer that follows the following rules"""
        result = []
        line_num = 1
        stemmer = PorterStemmer()

        for line in file_reader:
            parsed_line = re.findall(r"[\w']+|[.,!?;#]", line.replace("\t", ' ').replace("\n", ' '))
            parsed_line = filter(None, parsed_line)
            for token in parsed_line:
                if isfloat(token):
                    result.append(token + ' DOUBLE ' + str(line_num))
                elif isint(token):
                    result.append(token + ' INT ' + str(line_num))
                elif token in set(string.punctuation):
                    result.append(token + ' OP ' + str(line_num))
                else:
                    if line[0] == 'W':
                        result.append(token + ' STRING ' + str(line_num) + ' ' + stemmer.stem(token))
                    else:
                        result.append(token + ' STRING ' + str(line_num))

            line_num += 1

        result.append("ENDFILE\n")
        return result
