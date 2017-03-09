#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-1-23

import dataStructure.common.node as BasicNode
from dataStructure.common.test_data import rand
from dataStructure.tree.binary_tree_by_linklist import BinaryTreeByLinkList


class IntTrie(BinaryTreeByLinkList):
    # 小端树，整数化为2进制，然后由右向左写
    # 左侧为奇数，右侧偶数
    class Node(BasicNode.Node):
        # key 必须为整数
        def __init__(self, key=None, value=None):
            BasicNode.Node.__init__(self, key, value)

        def __str__(self):
            return '%s' % (self.value)

    def __init__(self):
        self.root = self.Node()

    def insert(self, k, v=None):  # 迭代
        p = self.root
        key = k
        while p is self.root or k != 0:
            if k & 1 == 0:  # 偶数
                if p.left is None:
                    p.left = self.Node()
                p = p.left
            else:  # 奇数
                if p.right is None:
                    p.right = self.Node()
                p = p.right
            k = k >> 1  # 右移一位，整除2
        p.key = key
        p.value = v

    def insert2(self, node, k, v=None):  # 递归
        if node is not self.root and k == 0:
            node.key = 'y'
            node.value = v
        elif k & 1:
            if node.right is None:
                node.right = self.Node()
            self.insert2(node.right, k / 2, v)
        else:
            if node.left is None:
                node.left = self.Node()
            self.insert2(node.left, k / 2, v)

    def search(self, k):
        p = self.root
        while p is self.root or k != 0 and p is not None:
            if k & 1:
                p = p.right
            else:
                p = p.left
            k = k >> 1
        if p is not None:
            return p.value
        else:
            return None

    def test(self):
        # rand = [4, 6, 7, 0, 4]
        print rand
        for i in rand:
            self.insert(i, i)
            # self.insert2(self.root, i, i)
        self.print_tree()
        print self.search(5)


if __name__ == '__main__':
    t = IntTrie()
    t.test()
