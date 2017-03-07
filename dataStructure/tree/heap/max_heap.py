#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3

from dataStructure.tree.completely_tree import *


class MaxHeap(CompletelyTree):
    ## 最大堆，page 137，from《数据结构》

    def append(self, key):
        node = Node(key)
        self.b_tree.append(node)
        tail = len(self.b_tree) - 1
        while tail > 1:
            parent = tail / 2
            # print self.b_tree[parent], self.b_tree[tail]
            if self.b_tree[parent].key >= self.b_tree[tail].key:
                break
            self.b_tree[tail], self.b_tree[parent] = self.b_tree[parent], self.b_tree[tail]
            tail = parent
        self.b_tree[tail] = node

    def pop(self):
        if self.len() == 0:
            return None
        item = self.b_tree[1]
        tail = self.len() - 1
        tmp = self.b_tree[tail]
        self.b_tree.pop()
        tail -= 1
        parent = 1
        child = 2
        while (child < tail):
            if child < tail and self.left(parent).key < self.right(parent).key:
                child += 1
            if tmp.key >= self.b_tree[child].key:
                break
            self.b_tree[parent] = self.b_tree[child]
            parent = child
            child *= 2
        self.b_tree[parent] = tmp
        return item

    def test(self):
        rand_list = gen_rand_list(14, 1, 999)
        print rand_list
        for i in rand_list:
            self.append(i)
            # self.print_bt()
            # print '-----'

        print self.pop().key
        print '==============================='
        self.print_bt()
        print self.pop().key
        print '==============================='
        self.print_bt()


class Heapify(CompletelyTree):
    # 2017.02.6 《算法新解》
    class Node(Node):
        def __cmp__(self, other):
            return cmp(self.key, other.key)

    def __init__(self):
        self.b_tree = []

    def comp(self, x, y):
        #  通过方法控制排序，最大最小堆用一套代码实现
        return x < y  # 最小堆

    def heapify(self, array, index):
        # 把堆调整为合法，条件是index的两个子树都是合法的堆
        # 数组索引从1开始
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
            self.b_tree.append(self.Node(i))

    def pop(self):
        head = self.b_tree[1]
        tail = self.len() - 1
        self.b_tree[1] = self.b_tree[tail]
        self.b_tree.pop()
        self.heapify(self.b_tree, 1)
        return head

    def test(self):
        rand_list = gen_rand_list(10, 0, 500)
        rand_list.insert(0, None)
        print rand_list
        self.build_heapify(rand_list)
        for i in self.b_tree:
            print i,
        print ''
        self.print_bt()
        for i in range(3):
            print '====='
            print self.pop()
            self.print_bt()


if __name__ == '__main__':
    bt = MaxHeap()
    bt.test()

    bt = Heapify()
    bt.test()
