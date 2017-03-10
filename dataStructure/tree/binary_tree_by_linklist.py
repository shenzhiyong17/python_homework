#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-2

from dataStructure.tree.node import Node


class BinaryTreeByLinkList():
    root = None
    length = 1

    def __init__(self, root=Node()):
        self.root = root

    def pre_order(self, node, r=None):
        if r is None:
            r = []
        res = r
        if node:
            res.append(node.key)
            self.pre_order(node.left, res)
            self.pre_order(node.right, res)
        return res

    def in_order(self, node, r=None):
        if r is None:
            r = []
        res = r
        if node:
            self.in_order(node.left, res)
            res.append(node.key)
            self.in_order(node.right, res)
        return res

    def len(self, node, length=1, index=1):
        if index > length:
            self.length = index
        if node:
            self.len(node.left, self.length, index * 2)
            self.len(node.right, self.length, index * 2)
        return self.length

    def ch2arrary(self, node, index=0, res=None):
        if res is None:
            length = self.len(self.root)
            res = [None] * (length + 1)
        if node:
            res[index] = node
            self.ch2arrary(node.left, index * 2, res)
            self.ch2arrary(node.right, index * 2 + 1, res)
        return res

    def print_tree(self, tree_list=None):
        if tree_list is None:
            tree_list = self.ch2arrary(self.root, 1)
        if tree_list[1] is None:
            return
        while tree_list[-1] is None or tree_list[-1].key is None:
            tree_list.pop()
        level = 1
        index = 1
        node = tree_list[index]
        length = len(tree_list) - 1
        tmp = length
        while tmp > 1:
            tmp /= 2
            level += 1
        max_leaf = 2 ** (level - 1)
        tabs = max_leaf - 1
        for i in range(1, level + 1):
            lever_leaf_num = 2 ** (i - 1)
            j = 0
            while j < lever_leaf_num and length > 0:
                tmp = str(node).replace('None', '-')
                print '\t' * tabs + '%4s' % tmp + '\t' * (tabs + 1),
                length -= 1
                index += 1
                if index >= len(tree_list):
                    print '\n================================'
                    return
                node = tree_list[index]
                if not node:
                    node = Node()
                j += 1
            print '\n'
            tabs /= 2
        print '================================'


if __name__ == '__main__':
    bt = BinaryTreeByLinkList()
    p = bt.root
    p.key = 0
    p.right = Node(1)
    p = p.right
    p.left = Node()
    p = p.left
    p.right = Node(5)
    p = bt.root
    p.left = Node()
    p = p.left
    p.left = Node()
    p = p.left
    p.right = Node(4)
    bt.print_tree()
