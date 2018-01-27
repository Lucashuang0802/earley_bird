import re

class Validator:
            
    @staticmethod
    def validate_grammar(line):
        '''Returns a Grammar instance created from a text file.
           The file lines should have the format:
               lhs : outcome | outcome | outcome'''

        # set up regex
        grammar = "[a-zA-Z-]+"
        left_production = grammar
        right_production = "{0}(\s*{1})*(\s*\|\s*{2}(\s*{3})*)*\s*".format(grammar, grammar, grammar, grammar)
        p = re.compile("{0}\s*:\s*{1}".format(left_production, right_production))
        if p.match(line):
            return True
        return False
