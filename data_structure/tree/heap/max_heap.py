#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3


from data_structure.tree.completely_tree import *


class MaxHeap(CompletelyTree):
    # 最大堆，page 137，from《数据结构》

    def __init__(self):
        CompletelyTree.__init__(self)

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

    def pop(self):
        if self.len() <= 1:
            return None
        if self.len() == 2:
            return self.b_tree.pop(-1)
        res = self.b_tree[1]
        tmp = self.b_tree.pop()
        parent = 1
        child = 2
        while self.is_in(child):
            if self.is_in(child + 1) and self.b_tree[child] < self.b_tree[child + 1]:
                child += 1
            if tmp >= self.b_tree[child]:
                break
            self.b_tree[parent] = self.b_tree[child]
            parent = child
            child *= 2
        self.b_tree[parent] = tmp
        return res

    def max_heap_test(self):
        # rand = [82, 61, 80, 50, 66, 5, 84, 6, 94, 99, 61, 6, 73, 69, 24, 55, 77, 77, 26, 21]
        print "max heap rand:", rand
        for i in rand:
            self.add(i)
        self.print_tree()
        order = []
        while self.len() > 1:
            order.append(self.pop())
        sort = sorted(rand, reverse=True)
        assert sort == self.list(order)


if __name__ == '__main__':
    bt = MaxHeap()
    bt.max_heap_test()
