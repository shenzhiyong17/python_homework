#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-02-24
from data_structure.common.test_data import *
from data_structure.tree.binary_tree_by_arrary import *

N_INF = 9999


class ChampionTree(BinaryTreeByArray):
    # 锦标赛树，或称冠军树，用于快速选择排序
    # 将待排序元素构建成锦标赛树，冠军位于树根
    # 取出树根后自顶向下将最大值替换为 N_INF（正负无穷）
    # 自底向上沿刚才路径回溯，找出新冠军，将其置于树根

    def __init__(self, array=[]):
        self.data_length = len(array)
        BinaryTreeByArray.__init__(self, len(array) * 2)

    def built_tree(self, array):
        index = len(array)
        for i in array:
            self.b_tree[index] = Node(i)
            index += 1
        p = len(array) - 1
        index = p
        for i in range(p, 0, -1):
            self.b_tree[index] = min(self.b_tree[index * 2], self.b_tree[index * 2 + 1])
            index -= 1

    def pop(self):
        result = self.b_tree[1].key
        index = 1
        while True:
            self.b_tree[index] = Node(N_INF)
            index *= 2
            if index >= self.size:
                break
            if index + 1 < self.size and self.b_tree[index] > self.b_tree[index + 1]:
                index += 1
        index /= 2
        while index > 1:
            index /= 2
            self.b_tree[index] = min(self.b_tree[index * 2], self.b_tree[index * 2 + 1])
        return result

    def sort(self):
        array = []
        for i in range(self.data_length):
            array.append(self.pop())
        return array

    def test(self, test_data=rand_list(40)):
        print test_data
        self.__init__(test_data)
        self.built_tree(test_data)
        sort = self.sort()
        assert sort == sorted(test_data)


if __name__ == '__main__':
    ct = ChampionTree()
    ct.test()
