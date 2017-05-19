#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-3-9

from dataStructure.basic.single_link_list import *


class Queue:

    def __init__(self):
        self.head = Node()
        self.tail = self.head

    def enqueue(self, key):
        node = Node(key)
        node.next = self.tail
        self.tail = node

    def dequeue(self):
        res = self.head.key
        self.head = self.head.next
        return res

