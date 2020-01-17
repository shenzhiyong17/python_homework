#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-18

from data_structure.common.gen_rand import gen_rand_list
from data_structure.tree.binary_tree_by_linklist import BinaryTreeByLinkList
import data_structure.tree.node as BasicNode


class Leftist(BinaryTreeByLinkList):
    # 最小左高树，最小树，左子树最小深度大于右子树最小深度，page 284

    class Node(BasicNode.Node):
        shortest = 1

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
        self.root = self.union(self.root, self.Node(key))

    def delete(self, node):
        node = self.union(node.left, node.right)
        return node

    def leftist_test(self):
        rand = gen_rand_list(10, 1, 99)
        # rand = [97, 56, 59, 94, 13]
        print rand
        self.root = self.Node(rand.pop(0))
        for i in rand:
            self.insert(i)
        self.print_tree()
        self.root.left = self.delete(self.root.left)
        self.print_tree()


if __name__ == '__main__':
    leftist = Leftist()
    leftist.leftist_test()
