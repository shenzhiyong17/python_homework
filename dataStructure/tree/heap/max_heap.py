#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3

from dataStructure.tree.completely_tree import *


class MaxHeap(CompletelyTree):
    ## 最大堆，page 137，from《数据结构》

    def add(self, key):
        node = Node(key)
        self.b_tree.append(node)
        tail = self.len() - 1
        while tail > 1:
            parent = tail / 2
            if self.b_tree[parent] >= self.b_tree[tail]:
                break
            self.b_tree[tail], self.b_tree[parent] = self.b_tree[parent], self.b_tree[tail]
            tail = parent
        self.b_tree[tail] = node

    def pop(self):
        if self.len() <= 1:
            return None
        if self.len() == 2:
            return self.b_tree.pop(-1)
        max = self.b_tree[1]
        tmp = self.b_tree.pop()
        tail = self.len() - 1
        parent = 1
        child = 2
        while (child <= tail):
            if self.is_in(child + 1) and self.b_tree[child] < self.b_tree[child + 1]:
                child += 1
            if tmp >= self.b_tree[child]:
                break
            self.b_tree[parent] = self.b_tree[child]
            parent = child
            child *= 2
        self.b_tree[parent] = tmp
        return max

    def test(self):
        # rand = [82, 61, 80, 50, 66, 5, 84, 6, 94, 99, 61, 6, 73, 69, 24, 55, 77, 77, 26, 21]
        print rand
        for i in rand:
            self.add(i)

        order = []
        while self.len() > 1:
            order.append(self.pop())
        sort = sorted(rand, reverse=True)
        assert sort == self.list(order)


class Heapify(CompletelyTree):
    # 2017.02.6 《算法新解》

    def __init__(self):
        # 把无序数组整个放进来再调整，只能在无序数组头部加None，不能初始化在self.b_tree里
        self.b_tree = []

    def comp(self, x, y):
        #  通过方法控制排序，最大最小堆用一套代码实现
        return x < y  # 最小堆

    def heapify(self, array, index):
        # 把堆调整为合法，条件是index的两个子树都是合法的堆
        # 数组索引从1开始
        # 原地调整数组
        n = len(array)
        while True:
            l = index * 2
            r = index * 2 + 1
            smallest = index
            if l < n and self.comp(array[l], array[smallest]):
                smallest = l
            if r < n and self.comp(array[r], array[smallest]):
                smallest = r
            if smallest != index:
                array[index], array[smallest] = array[smallest], array[index]
                index = smallest
            else:
                return array

    def build_heapify(self, array):
        n = len(array)
        for i in range(n / 2, 0, -1):
            array = self.heapify(array, i)
        for i in array:
            self.b_tree.append(Node(i))

    def pop(self):
        head = self.b_tree[1]
        tail = self.len() - 1
        self.b_tree[1] = self.b_tree[tail]
        self.b_tree.pop()
        self.heapify(self.b_tree, 1)
        return head

    def test(self):
        # rand = [26, 68, 10]
        print rand
        self.build_heapify([None,] + rand)
        order = []
        while self.len() > 1:
            order.append(self.pop())
        sort = sorted(rand, reverse=False)
        assert sort == self.list(order)


if __name__ == '__main__':
    bt = MaxHeap()
    bt.test()

    bt = Heapify()
    bt.test()
