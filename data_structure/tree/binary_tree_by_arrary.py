#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3
# ----- 数组实现普通二叉树 -----
# ----- root为1， 0位不用 -----

import copy

from data_structure.common.gen_rand import *


class Node:
    def __init__(self, key=None):
        self.key = key

    def __str__(self):
        return '%s' % self.key

    def __cmp__(self, other):
        return cmp(self.key, other.key)


class BinaryTreeByArray:
    def __init__(self, size=100):
        self.size = size
        self.b_tree = [None] * size

    def parent(self, index):
        if index >= 2:
            return self.b_tree[index / 2]
        else:
            return None

    def left(self, index):
        return self.b_tree[index * 2] if index * 2 < len(self.b_tree) else None

    def right(self, index):
        return self.b_tree[index * 2 + 1] if index * 2 + 1 < len(self.b_tree) else None

    def modify(self, key, index):
        if 0 < index < self.size:
            self.b_tree[index] = Node(key)

    # 前序
    def pre_order(self, index=1, res=None):
        if res is None:
            res = []
        node = self.b_tree[index]
        if isinstance(node, Node):
            res.append(node.key)
            self.pre_order(index * 2, res)
            self.pre_order(index * 2 + 1, res)
        return res

    # 中序
    def in_order(self, index=1, res=None):
        if res is None:
            res = []
        if index >= self.size:
            raise RuntimeError("index 超出范围")
        node = self.b_tree[index]
        if node is not None:
            self.in_order(index * 2, res)
            res.append(node.key)
            self.in_order(index * 2 + 1, res)
        return res

    # 后序
    def post_order(self, index=1, res=None):
        if res is None:
            res = []
        node = self.b_tree[index]
        if isinstance(node, Node):
            self.post_order(index * 2, res)
            self.post_order(index * 2 + 1, res)
            res.append(node.key)
        return res

    # 层序
    def level_order(self):
        queue = []
        res = []
        index = 1
        if len(self.b_tree) <= 1:
            return res
        queue.append(self.b_tree[index])
        while len(queue) > 0:
            node = queue.pop(0)
            if node is not None:
                res.append(node.key)
                queue.append(self.left(index))
                queue.append(self.right(index))
            index += 1
        return res

    def print_tree(self):
        if len(self.b_tree) <= 1:
            return
        tree = copy.copy(self.b_tree)
        while not tree[-1]:
            tree.pop()
        level = 1
        index = 1
        node = tree[index]
        length = len(tree) - 1
        # print length
        tmp = length
        while tmp > 1:
            tmp /= 2
            level += 1
        max_leaf = 2 ** (level - 1)
        tabs = max_leaf - 1
        for i in range(1, level + 1):
            level_leaf_num = 2 ** (i - 1)
            for j in range(level_leaf_num):
                print '\t' * tabs + '%4s' % node.key + '\t' * (tabs + 1),
                length -= 1
                index += 1
                try:
                    node = self.b_tree[index]
                except IndexError:
                    node = Node('-')
                if not node:
                    node = Node('-')
            print '\n'
            tabs /= 2
        print '==============================='

    def list(self, a=None):
        if a is None:
            a = self.b_tree[1:]
        res = []
        for i in a:
            res.append(i.key)
        return res

    def test(self):
        for i in range(15):
            self.modify(random.randint(1, 99), i)
        self.b_tree[4] = None
        self.print_tree()
        print "level_order:", self.level_order()
        print "  pre_order:", self.pre_order()
        print "   in_order:", self.in_order()
        print " post_order:", self.post_order()


if __name__ == '__main__':
    bt = BinaryTreeByArray()
    bt.test()
