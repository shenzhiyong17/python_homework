#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-17

import math

from dataStructure.tree.completely_tree import *


class Deap(CompletelyTree):
    # 双端堆，左子树为最小堆，右子树为最大堆，根为空
    # i是左子树节点，j是右子树对应节点，如果j为空，则j为i的父节点的对应节点，且 i < j
    def __init__(self):
        CompletelyTree.__init__(self)
        self.b_tree.append(Node(' '))  # 根，即b_tree[1]为空

    def __max_heap(self, index):
        while index > 3:
            index /= 2
        if index == 2:
            return False
        return True

    def __partner(self, left=0, right=0):
        # 查找对应节点位置
        if left > 1:
            t = int(math.log(left, 2) - 1)
            t = 2 ** t
            right = left + t
            if not self.is_in(right):
                right /= 2
            return right
        if right > 1:
            t = int(math.log(right, 2) - 1)
            t = 2 ** t
            left = right - t
            return left
        raise

    def __min_insert(self, index, key):
        if index == 2:
            try:
                self.b_tree[index] = Node(key)
            except IndexError:
                self.b_tree.append(Node(key))
            return
        parent = index / 2
        if index > self.len() - 1:
            self.b_tree.append(None)
        while self.b_tree[parent].key > key and parent >= 2:
            self.b_tree[index] = self.b_tree[parent]
            index = parent
            parent /= 2
        self.b_tree[index] = Node(key)

    def __max_insert(self, index, key):
        if index == 3:
            try:
                self.b_tree[index] = Node(key)
            except IndexError:
                self.b_tree.append(Node(key))
            return
        if not self.is_in(index):
            self.b_tree.append(None)
        parent = index / 2
        while self.b_tree[parent].key < key and parent >= 3:
            self.b_tree[index] = self.b_tree[parent]
            index = parent
            parent /= 2
        self.b_tree[index] = Node(key)

    def __insert(self, index, key):
        parent = index / 2
        if not self.b_tree[parent]:
            raise
        if self.__max_heap(index):
            i = self.__partner(right=index)
            if not self.is_in(index * 2) and self.is_in(i * 2):
                i *= 2
                if self.is_in(i + 1) and self.b_tree[i] < self.b_tree[i + 1]:
                    i += 1
            if self.b_tree[i].key > key:
                self.b_tree[index] = self.b_tree[i]
                self.__min_insert(i, key)
            else:
                self.__max_insert(index, key)
        else:
            j = self.__partner(left=index)
            if self.b_tree[j].key < key:
                self.b_tree[index] = self.b_tree[j]
                self.__max_insert(j, key)
            else:
                self.__min_insert(index, key)

    def append(self, key):
        if self.len() == 2:  # 最小堆根节点
            self.b_tree.append(Node(key))
            return
        if self.len() == 3:  # 最大堆根节点
            if self.b_tree[2].key > key:
                self.b_tree.insert(2, Node(key))
            else:
                self.b_tree.append(Node(key))
            return
        index = self.len()
        if self.__max_heap(index):
            i = self.__partner(right=index)
            if self.b_tree[i].key > key:
                self.b_tree.append(self.b_tree[i])
                self.__min_insert(i, key)  # 把原先的i替换成新node，然后适配
            else:
                self.__max_insert(index, key)  # append在最后，然后适配
        else:
            j = self.__partner(left=index)
            if self.b_tree[j].key < key:
                self.b_tree.append(self.b_tree[j])
                self.__max_insert(j, key)
            else:
                self.__min_insert(index, key)

    def delete_min(self):
        last = self.b_tree.pop(-1)
        if self.len() <= 2:
            return last
        res = self.b_tree[2]
        index = 4
        while self.is_in(index):
            parent = index / 2
            if self.is_in(index + 1):
                if self.b_tree[index].key > self.b_tree[index + 1].key:
                    index += 1
            self.b_tree[parent] = self.b_tree[index]
            index *= 2
        index /= 2
        self.__insert(index, last.key)
        return res

    def delete_max(self):
        last = self.b_tree.pop(-1)
        if self.len() <= 3:
            return last
        res = self.b_tree[3]
        index = 6
        while self.is_in(index):
            parent = index / 2
            if self.is_in(index + 1):
                if self.b_tree[index].key < self.b_tree[index + 1].key:
                    index += 1
            self.b_tree[parent] = self.b_tree[index]
            index *= 2
        index /= 2
        self.__insert(index, last.key)
        return res

    def test(self):
        # rand = [65, 13, 96, 96, 39, 35, 51, 23, 60, 66, 90, 38, 74, 67, 33, 14, 31, 88, 68, 74]
        print rand

        # 降序测试
        for v in rand:
            self.append(v)
        order = []
        while self.len() > 2:
            order.append(self.delete_max())
        sort = sorted(rand, reverse=True)
        assert sort == self.list(order)

        # 升序测试
        for v in rand:
            self.append(v)
        order = []
        while self.len() > 2:
            order.append(self.delete_min())
        sort = sorted(rand, reverse=False)
        assert sort == self.list(order)


if __name__ == '__main__':
    deap = Deap()
    deap.test()
