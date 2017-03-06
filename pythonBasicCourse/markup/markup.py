#!/usr/bin/env python
#coding=utf-8
# 2016-4-12
# 20章，即时标记

import sys, re
from handler import *
from rules import *
from util import *

class Parser:

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler):
                        break
        self.handler.end('document')

class BasicTextParser(Parser):

    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListItemRule())
        self.addRule(ListRule())
        # self.addRule(HeadingRule())
        self.addRule(TitleRule())
        # self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\./a-zA-Z]+)', 'url')
        self.addFilter(r'([a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'email')


if __name__ == '__main__':
    handler = HTMLRendere()
    parser = BasicTextParser(handler)
    parser.parse(open('text_input.txt'))
