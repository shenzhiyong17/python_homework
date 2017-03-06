#!/usr/bin/env python
#coding=utf-8
# 2016-4-12

class Rule:

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    '''
    标题占一行
    '''
    type = 'heading'

    def condition(self, block):
        return not '\n' in block and not block[-1] == ':' and len(block) <=70

class TitleRule(HeadingRule):
    '''
    题目是文档的第一个标题
    '''
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first : return False
        self.first = False
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    type = 'listitem'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:])
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    type = 'list'
    inside = False

    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            self.inside = True
            handler.start(self.type)
        elif self.inside and not ListItemRule.condition(self, block):
            self.inside = False
            handler.end(self.type)
        return False

class ParagraphRule(Rule):
    type = 'paragraph'

    def condition(self, block):
        return True

