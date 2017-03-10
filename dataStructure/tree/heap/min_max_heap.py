#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-14

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

    def __verify_min(self, index, key):
        if not self.is_in(index):
            self.b_tree.append(Node(key))
        grandparent = index / 4
        while grandparent >= 1:
            if key < self.b_tree[grandparent].key:
                self.b_tree[index] = self.b_tree[grandparent]
                index = grandparent
                grandparent /= 4
            else:
                break
        self.b_tree[index] = Node(key)

    def __verify_max(self, index, key):
        if not self.is_in(index):
            self.b_tree.append(Node(key))
        grandparent = index / 4
        while grandparent >= 1:
            if key > self.b_tree[grandparent].key:
                self.b_tree[index] = self.b_tree[grandparent]
                index = grandparent
                grandparent /= 4
            else:
                break
        self.b_tree[index] = Node(key)

    def __min_child_grandchild(self, index):
        #  找出儿孙中最小元素位置
        level = self.level(index)
        left = index * 2
        right = index * 2 + 1
        grandchild = index * 4
        if not self.is_in(grandchild) or level == 'max':
            if self.is_in(right):
                if self.b_tree[right] < self.b_tree[left]:
                    return right
            if self.is_in(left):
                return left
            else:
                return index
        elif level == 'min':
            min = self.b_tree[right].key
            res = right
            for i in range(grandchild, grandchild + 4):
                if not self.is_in(i):
                    break
                if self.b_tree[i].key < min:
                    min = self.b_tree[i].key
                    res = i
            return res

    def __max_child_grandchild(self, index):
        level = self.level(index)
        left = index * 2
        right = index * 2 + 1
        grandchild = index * 4
        if not self.is_in(grandchild) or level == 'min':
            if self.is_in(right):
                if self.b_tree[right] > self.b_tree[left]:
                    return right
            if self.is_in(left):
                return left
            else:
                return index
        elif level == 'max':
            max = self.b_tree[right].key
            res = right
            for i in range(grandchild, grandchild + 4):
                if not self.is_in(i):
                    break
                if self.b_tree[i].key > max:
                    max = self.b_tree[i].key
                    res = i
            return res

    def insert(self, key):
        index = self.len()
        parent = self.b_tree[index / 2]
        if not parent:
            self.b_tree.append(Node(key))
        else:
            parent_index = index / 2
            parent_level = self.level(parent_index)
            if parent_level == 'min':
                if key < parent.key:
                    self.b_tree.append(parent)
                    self.__verify_min(parent_index, key)
                else:
                    self.__verify_max(index, key)
            if parent_level == 'max':
                if key > parent.key:
                    self.b_tree.append(parent)
                    self.__verify_max(parent_index, key)
                else:
                    self.__verify_min(index, key)

    def delete_min(self):
        root = self.b_tree[1]
        item = self.pop()
        i = 1
        if self.len() > 1:
            while (i <= self.len() / 2):
                k = self.__min_child_grandchild(i)
                if item <= self.b_tree[k]:
                    break
                self.b_tree[i] = self.b_tree[k]
                if (k <= 2 * i + 1):
                    i = k
                    break
                parent = k / 2
                if (item.key > self.b_tree[parent].key):
                    self.b_tree[parent], item = item, self.b_tree[parent]
                i = k
            self.b_tree[i] = item
        return root

    def delete_max(self):
        item = self.pop()
        if self.len() <= 1:
            return item
        i = self.__max_child_grandchild(1)
        max = self.b_tree[i]
        if item > max:
            return item
        last = self.len() / 2
        while (i <= last):
            k = self.__max_child_grandchild(i)
            if item >= self.b_tree[k]:
                break
            self.b_tree[i] = self.b_tree[k]
            if (k <= 2 * i + 1):
                i = k
                break
            parent = k / 2
            if (item.key < self.b_tree[parent].key):
                self.b_tree[parent], item = item, self.b_tree[parent]
            i = k
        self.b_tree[i] = item

        return max

    def test(self):
        rand = [3, 77, 64, 97, 16, 25, 22, 77, 98, 53, 28, 24, 2, 93, 3, 32, 68, 73, 87]
        # rand = [2, 3]
        print rand
        # 验证升序
        for i in rand:
            self.insert(i)
        order = []
        while self.len() > 1:
            order.append(self.delete_min())
        sort = sorted(rand)
        assert sort == self.list(order)

        # 验证降序
        for i in rand:
            self.insert(i)
        order = []
        while self.len() > 1:
            order.append(self.delete_max())
        sort = sorted(rand, reverse=True)
        assert sort == self.list(order)


if __name__ == '__main__':
    bt = MinMaxHeap()
    bt.test()
