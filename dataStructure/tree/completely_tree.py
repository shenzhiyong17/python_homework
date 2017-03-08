#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3

from binary_tree_by_arrary import *
from dataStructure.common.test_data import rand


class CompletelyTree(BinaryTreeByArray):
    # b_tree[0] 为空，index 从1开始
    def __init__(self):
        # 满二叉树没用空元素，不用设置None占位，不用设置max值
        self.b_tree = [None, ]

    def len(self):
        return len(self.b_tree)

    def is_in(self, index):
        return index < self.len() - 1

    def modify(self, key, index):
        if index > 1 and index < self.len():
            self.b_tree[index].key = key

    def append(self, node):
        self.b_tree.append(node)

    def pop(self):
        # 弹出最后一个元素
        return self.b_tree.pop()

    def test(self):
        print rand
        for i in rand:
            self.append(Node(i))
        self.modify('ss', 5)
        self.print_bt()
        print self.len()
        print self.pop()
        self.print_bt()
        print self.level_order()


if __name__ == '__main__':
    bt = CompletelyTree()
    bt.test()
