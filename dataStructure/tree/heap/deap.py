#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-17

import math

from dataStructure.tree.completely_tree import *

# 去掉数组二叉树中 max 字段后引出问题未解

class Deap(CompletelyTree):
    ## 双端堆，左子树为最小堆，右子树为最大堆,根为空
    def __init__(self, max=100):
        CompletelyTree.__init__(self)
        self.b_tree[1] = Node(' ')

    def max_heap(self, index):
        while index > 3:
            index /= 2
        if index == 2:
            return False
        return True

    def partner(self, left=0, right=0):
        n = self.len()
        if left > 1:
            t = int(math.log(left, 2) - 1)
            t = 2 ** t
            right = left + t
            if right > n:
                right /= 2
            return right
        if right > 1:
            t = int(math.log(right, 2) - 1)
            t = 2 ** t
            left = right - t
            return left
        raise

    def min_insert(self, index, key):
        if index == 2:
            self.b_tree[index] = Node(key)
            return
        parent = index / 2
        while self.b_tree[parent].key > key and parent >= 2:
            self.b_tree[index] = self.b_tree[parent]
            index = parent
            parent /= 2
        self.b_tree[index] = Node(key)

    def max_insert(self, index, key):
        if index == 3:
            self.b_tree[index] = Node(key)
            return
        parent = index / 2
        while self.b_tree[parent].key < key and parent >= 3:
            self.b_tree[index] = self.b_tree[parent]
            index = parent
            parent /= 2
        self.b_tree[index] = Node(key)

    def insert(self, index, key):
        parent = index / 2
        if parent < 2:
            self.b_tree[index] = Node(key)
            return
        if not self.b_tree[parent]:
            raise
        if self.max_heap(index):
            i = self.partner(right=index)
            if self.b_tree[i].key > key:
                self.b_tree[index] = self.b_tree[i]
                self.min_insert(i, key)
            else:
                self.max_insert(index, key)
        else:
            j = self.partner(left=index)
            if self.b_tree[j].key < key:
                self.b_tree[index] = self.b_tree[j]
                self.max_insert(j, key)
            else:
                self.min_insert(index, key)

    def append(self, key):
        if not self.b_tree[2]:
            self.b_tree[2] = Node(key)
            return
        if not self.b_tree[3]:
            if self.b_tree[2].key > key:
                self.b_tree[3] = self.b_tree[2]
                self.b_tree[2] = Node(v)
            else:
                self.b_tree[3] = Node(v)
            return
        index = self.len() + 1
        if self.max_heap(index):
            i = self.partner(right=index)
            if self.b_tree[i].key > key:
                self.b_tree[index] = self.b_tree[i]
                self.min_insert(i, key)
            else:
                self.max_insert(index, key)
        else:
            j = self.partner(left=index)
            if self.b_tree[j].key < key:
                self.b_tree[index] = self.b_tree[j]
                self.max_insert(j, key)
            else:
                self.min_insert(index, key)

    def delete_min(self):
        n = self.len()
        last = self.b_tree[n].key
        res = self.b_tree[2]
        index = 4
        while self.b_tree[index]:
            parent = index / 2
            if self.b_tree[index + 1]:
                if self.b_tree[index].key > self.b_tree[index + 1].key:
                    index += 1
            self.b_tree[parent] = self.b_tree[index]
            index *= 2
        index /= 2
        self.insert(index, last)
        self.b_tree[n] = None
        return res

    def delete_max(self):
        n = self.len()
        last = self.b_tree[n].key
        res = self.b_tree[3]
        index = 3
        parent = 3
        while self.b_tree[index]:
            parent = index / 2
            if self.b_tree[index + 1]:
                if self.b_tree[index].key < self.b_tree[index + 1].key:
                    index += 1
            self.b_tree[parent] = self.b_tree[index]
            index *= 2
        index /= 2
        self.insert(index, last)
        self.b_tree[n] = None
        return res


if __name__ == '__main__':
    deap = Deap()
    # rand = [48, 31, 23, 32, 79, 18, 41, 34, 57, 45, 1, 40, 27, 30, 98, 99, 40, 87, 26, 56, 98, 50, 79, 17, 21, 27, 75, 68, 55, 78]
    rand = gen_rand_list(30, 1, 99)
    print rand
    for v in rand:
        deap.append(v)
    deap.print_bt()
    deap.delete_min()
    deap.print_bt()
    deap.delete_max()
    deap.print_bt()
