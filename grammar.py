#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys

class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __len__(self):
        return len(self.rhs)

    def __repr__(self):
        return "<Rule {0} -> {1}>".format(self.lhs, ' '.join(self.rhs))

    def __getitem__(self, item):
        return self.rhs[item]

    def __cmp__(self, other):
        if self.lhs == other.lhs:
            if self.rhs == other.rhs:
                return 0
        return 1

class Grammar:
    def __init__(self):
        self.rules = {}

    def __repr__(self):
        st = '<Grammar>\n'
        for group in self.rules.values():
            for rule in group:
                st+= '\t{0}\n'.format(str(rule))
        st+= '</Grammar>'
        return st

    def __getitem__(self, lhs):
        if lhs in self.rules:
            return self.rules[lhs]
        else:
            return None

    def add_rule(self, rule):
        lhs = rule.lhs
        if lhs in self.rules:
            self.rules[lhs].append(rule)
        else:
            self.rules[lhs] = [rule]

    @staticmethod
    def from_file(filename):
        "reads grammar from file"
        try:
            lines = file(filename)
        except IOError as e:
            sys.stderr.write("Error reading file {0}\n".format(filename))
            sys.exit(1)

        grammar = Grammar()

        for line in lines:
            # ignore comments
            line = line[0:line.find('#')]
            if len(line) < 3:
                continue

            # lhs -> outcome | outcome | outcome
            rule = line.split('->')
            lhs = rule[0].strip()
            for outcome in rule[1].split('|'):
                rhs = outcome.strip()
                symbols = rhs.split(' ') if rhs else []
                r = Rule(lhs, symbols)
                grammar.add_rule(r)

        return grammar
