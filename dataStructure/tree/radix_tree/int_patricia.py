#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-1-24

import dataStructure.common.node as BasicNode
from dataStructure.common.test_data import rand
from dataStructure.tree.binary_tree_by_linklist import BinaryTreeByLinkList


class IntPatricia(BinaryTreeByLinkList):
    # Trie的加强简化版，通过 prefix 和 mask 缩短根到叶子节点的路径
    # 大端树，只有叶子节点存信息，branch节点存 叶子节点的 prefix和 mask

    id = 0  # Node 的全局变量，debug用

    class Node(BasicNode.Node):
        def __init__(self, key=None, value=None):
            BasicNode.Node.__init__(self, key, value)
            self.prefix = None
            self.mask = None
            self.id = IntPatricia.id    # 记录Node 生成顺序
            IntPatricia.id += 1

        def __str__(self):
            k, p, m = None, None, None
            if self.prefix:
                p = '{0:b}'.format(self.prefix)      # 二进制表示
            if self.mask:
                m = '{0:b}'.format(self.mask)
            if self.is_leaf():
                return '%s.%s' % (self.id, self.key)
            else:
                return '%s.%s.%s' % (self.id, p, m)

        def is_leaf(self):
            return self.left is None and self.right is None

        def get_prefix(self):  # 叶节点的prefix为key
            if self.prefix is None:
                return self.key
            else:
                return self.prefix

    def __init__(self):
        self.root = None

    def match(self, k, p, m):       # 判断key是否符合 mask与 prefix
        return ~(m - 1) & k == p    # ~按位取反，m-1取反后，高位全1，低位全0

    def zero(self, k, m):           # 判断key 的mask 后一位是0或1，以判断左右分支
        return (m >> 1 & k) == 0    # mask右移一位即所求位

    def lcp(self, x, y):            # 求xy 的最长公前缀和mask
        diff = (x ^ y)              # ^异或，找xy最大不同位，即mask的最大0位
        mask = 1
        while diff != 0:
            diff >>= 1
            mask <<= 1
        prefix = ~(mask - 1) & x    # 同 match
        return prefix, mask

    def branch(self, x, y):         # x与y prefix不同时，生成分支节点，该节点的两个分支为x、y，重新计算xy的prefix和mask
        node = self.Node()
        node.prefix, node.mask = self.lcp(x.get_prefix(), y.get_prefix())
        # print 'node.: %s.%s.%s' % (node.id, '{0:b}'.format(node.prefix), '{0:b}'.format(node.mask))
        if self.zero(x.key, node.mask):
            node.left = x
            node.right = y
        else:
            node.left = y
            node.right = x
        return node

    def insert(self, k, v):
        if self.root is None:
            self.root = self.Node(key=k, value=v)
            return
        y = self.root
        parent = None
        while True:
            if (not y.is_leaf()) and self.match(k, y.prefix, y.mask):   # 分支并且匹配
                parent = y
                if self.zero(k, y.mask):
                    y = y.left
                else:
                    y = y.right
            else:
                if y.is_leaf() and y.key == k:  # 已有key
                    y.value = v                 # 盖原值
                else:                           # prefix|mask 不匹配
                    branch = self.branch(self.Node(key=k, value=v), y)
                    if parent is None:
                        self.root = branch
                    else:
                        if parent.left is y:    # 取代原节点
                            parent.left = branch
                        else:
                            parent.right = branch
                break

    def search(self, key):
        if self.root is None:
            return None
        else:
            t = self.root
            while t:
                if not t.is_leaf() and self.match(key, t.prefix, t.mask):
                    if self.zero(key, t.mask):
                        t = t.left
                    else:
                        t = t.right
                else:
                    if t.is_leaf() and t.key == key:
                        return t
                    else:
                        return None


    def test(self):
        # rand = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        print rand
        for i in rand:
            self.insert(i, i)
            # self.print_tree()
        self.print_tree()
        x = 13
        if x in rand:
            assert self.search(x).key == x
        else:
            assert self.search(x) is None


if __name__ == '__main__':
    t = IntPatricia()
    t.test()
