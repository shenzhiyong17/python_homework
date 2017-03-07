#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-14

# 去掉数组二叉树中 max 字段后引出问题未解

from dataStructure.tree.completely_tree import *


class MinMaxHeap(CompletelyTree):
    ## 最大最小堆，根为最小，各层交替为最大最小层，page 274
    def level(self, index):
        tmp = 1
        level = 1
        while index > tmp:
            tmp = tmp * 2 + 1
            level += 1
        if (level % 2) == 0:
            return 'max'
        else:
            return 'min'

    def verify_min(self, index, key):
        grandparent = index / 4
        while grandparent >= 1:
            if key < self.b_tree[grandparent].key:
                self.b_tree[index] = self.b_tree[grandparent]
                index = grandparent
                grandparent /= 4
            else:
                break
        self.b_tree[index] = Node(key)

    def verify_max(self, index, key):
        grandparent = index / 4
        while grandparent >= 1:
            if key > self.b_tree[grandparent].key:
                self.b_tree[index] = self.b_tree[grandparent]
                index = grandparent
                grandparent /= 4
            else:
                break
        self.b_tree[index] = Node(key)

    def min_child_grandchild(self, index):
        level = self.level(index)
        left = index * 2
        right = index * 2 + 1
        grandchild = index * 4
        if not self.b_tree[grandchild] or level == 'max':
            if self.b_tree[right]:
                if self.b_tree[right].key < self.b_tree[left].key:
                    return right
            return left
        elif level == 'min':
            min = self.b_tree[grandchild].key
            res = grandchild
            for i in range(grandchild + 1, grandchild + 4):
                if not self.b_tree[i]:
                    break
                if self.b_tree[i].key < min:
                    min = self.b_tree[i].key
                    res = i
            return res

    def max_child_grandchild(self, index):
        level = self.level(index)
        left = index * 2
        right = index * 2 + 1
        grandchild = index * 4
        if not self.b_tree[grandchild] or level == 'min':
            if self.b_tree[right]:
                if self.b_tree[right].key > self.b_tree[left].key:
                    return right
            return left
        elif level == 'max':
            max = self.b_tree[grandchild].key
            res = grandchild
            for i in range(grandchild + 1, grandchild + 4):
                if not self.b_tree[i]:
                    break
                if self.b_tree[i].key > max:
                    max = self.b_tree[i].key
                    res = i
            return res

    def insert(self, key):
        self.b_tree.append(Node(key))
        index = self.len()
        parent = self.b_tree[index / 2]
        if not parent:
            self.b_tree[1] = Node(key)
        else:
            parent_index = index / 2
            level = self.level(parent_index)
            if level == 'min':
                if key < parent.key:
                    self.b_tree[index] = parent
                    self.verify_min(parent_index, key)
                else:
                    self.verify_max(index, key)
            if level == 'max':
                if key > parent.key:
                    self.b_tree[index] = parent
                    self.verify_max(parent_index, key)
                else:
                    self.verify_min(index, key)

    def delete_min(self):
        root = self.b_tree[1]
        item = self.pop()
        len = self.len()
        last = len / 2
        i = 1
        if len != 0:
            while (i <= last):
                k = self.min_child_grandchild(i)
                if item.key <= self.b_tree[k].key:
                    break
                self.b_tree[i] = self.b_tree[k]
                if (k <= 2 * i + 1):
                    i = k
                    break
                parent = k / 2
                if (item.key > self.b_tree[parent].key):
                    tmp = self.b_tree[parent]
                    self.b_tree[parent] = item
                    item = tmp
                i = k
            self.b_tree[i] = item
        return root

    def delete_max(self):
        item = self.pop()
        parent = self.parent(self.len())
        if not parent:
            return item
        if item.key < self.b_tree[2]:
            tmp = item
            item = self.b_tree[2]
            self.b_tree[2] = tmp
            return item
        i = self.max_child_grandchild(1)
        max = self.b_tree[i]
        last = self.len() / 2
        while (i <= last):
            k = self.max_child_grandchild(i)
            if item.key >= self.b_tree[k].key:
                break
            self.b_tree[i] = self.b_tree[k]
            if (k <= 2 * i + 1):
                i = k
                break
            parent = k / 2
            if (item.key < self.b_tree[parent].key):
                tmp = self.b_tree[parent]
                self.b_tree[parent] = item
                item = tmp
            i = k
        self.b_tree[i] = item
        return max


if __name__ == '__main__':
    bt = MinMaxHeap()
    # rand = [44,88,89,87]
    rand = gen_rand_list(10, 1, 99)
    for i in rand:
        bt.insert(i)
    bt.print_bt()
    print '======================================'
    print bt.delete_max().key
    bt.print_bt()
