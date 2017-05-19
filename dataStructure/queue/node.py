#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-3-9


class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

    def __str__(self):
        return "%s" % self.key
