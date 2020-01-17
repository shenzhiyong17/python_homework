#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.02.6 《算法新解》


from data_structure.tree.completely_tree import *


def comp(x, y):
    #  通过方法控制排序，最大最小堆用一套代码实现
    return x < y  # 最小堆


def heapify(array, index):
    # 把堆调整为合法，条件是index的两个子树都是合法的堆
    # 数组索引从1开始
    # 原地调整数组
    tail = len(array)
    while True:
        left = index * 2
        right = index * 2 + 1
        tmp = index
        if left < tail and comp(array[left], array[tmp]):
            tmp = left
        if right < tail and comp(array[right], array[tmp]):
            tmp = right
        if tmp != index:
            array[index], array[tmp] = array[tmp], array[index]
            index = tmp
        else:
            return array


class Heapify(CompletelyTree):

    def __init__(self):
        # 把无序数组整个放进来再调整，只能在无序数组头部加None，不能初始化在self.b_tree里
        self.b_tree = []

    def build_heapify(self, array):
        array = [None, ] + array
        n = len(array)
        for i in range(n / 2, 0, -1):
            array = heapify(array, i)
        for i in array:
            self.b_tree.append(Node(i))

    def pop(self):
        head = self.b_tree[1]
        tail = self.len() - 1
        self.b_tree[1] = self.b_tree[tail]
        self.b_tree.pop()
        heapify(self.b_tree, 1)
        return head

    def heapify_test(self):
        # rand = [26, 68, 10]
        print "heapify rand:", rand
        self.build_heapify(rand)
        self.print_tree()
        order = []
        while self.len() > 1:
            order.append(self.pop())
        sort = sorted(rand, reverse=False)
        assert sort == self.list(order)


if __name__ == '__main__':
    bt = Heapify()
    bt.heapify_test()
