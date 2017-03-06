#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-18

from dataStructure.common.gen_rand import gen_rand_list
from dataStructure.tree.binary_tree_by_linklist import BinaryTreeByLinkList


class Node():
    key = None
    left = None
    right = None
    shortest = 1

    def __init__(self, key=None):
        self.key = key


class Leftist(BinaryTreeByLinkList):
    # 最小左高树，最小树，左子树最小深度大于右子树最小深度，page 284

    def union(self, a, b):
        # 合并两颗最小左高树
        if a.key > b.key:
            tmp = a
            a = b
            b = tmp
        if a.right is None:
            a.right = b
        else:
            a.right = self.union(a.right, b)

        if a.left is None:
            a.left = a.right
            a.right = None
        elif a.left.shortest < a.right.shortest:
            tmp = a.left
            a.left = a.right
            a.right = tmp

        if a.right is None:
            a.shortest = 1
        else:
            a.shortest += 1
        return a

    def insert(self, key):
        self.root = self.union(self.root, Node(key))

    def delete(self, node):
        node = self.union(node.left, node.right)
        return node


if __name__ == '__main__':
    leftist = Leftist(Node(5))
    rand = gen_rand_list(10, 1, 99)
    # rand = [97, 56, 59, 94, 13]
    print rand
    for i in rand:
        leftist.insert(i)
    leftist.print_tree()
    print '====================================='
    leftist.root.left = leftist.delete(leftist.root.left)
    leftist.print_tree()
