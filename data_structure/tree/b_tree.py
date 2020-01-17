#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-1-30

import data_structure.tree.node as BasicNode
from common.Enum import Enum
from data_structure.common import gen_rand

class BTree():
    # B树，包括n个键值和n+1个子树，键值顺序单调递增
    # 所有叶子节点有相同深度
    # t为B树最小度数，每个节点最多有2t-1个键值，除根节点外，每个节点最少有t-1个键值
    class Node():
        def __init__(self, t):
            self.t = t
            self.keys = []
            self.children = []

        def is_leaf(self):
            return self.children == []

        def __str__(self):
            res = ''
            if self.is_leaf():
                for k in self.keys:
                    res += '%4s ' %k
            else:
                for k in self.keys:
                    res += '| %4s '%k
                res += '|'
            return res

    def __init__(self, t=3):
        self.t = t
        self.root = self.Node(t)

    def traversal(self, node, res=None):
        # 遍历树
        if res is None:
            res = []
        if node.is_leaf():
            res += node.keys()
        else:
            i = 0
            while node.keys[i]:
                res += self.traversal(node.children[i], res)
                res.append(node.keys[i])
                i += 1
            res += self.traversal(node.children[i], res)
        return res

    def insert(self, node, key):
        pass