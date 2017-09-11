#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-09-08


class Ball:
    _id = 0
    mark = None

    def __init__(self, id=0, weight=0):
        self.weight = weight
        self.id = id
        Ball._id += 1

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)

    def __int__(self):
        return self.weight

    def __str__(self):
        return 'ball %s, weight: %s, mark: %s' % (self.id, self.weight, self.mark)


def sum(array):
    res = 0
    for i in array:
        res += int(i)
    return res
