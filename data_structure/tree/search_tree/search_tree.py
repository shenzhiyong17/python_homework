#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3

from data_structure.common.test_data import rand
from data_structure.tree.binary_tree_by_linklist import *
from data_structure.tree.node import Node


class SearchTree(BinaryTreeByLinkList):
    # 搜索二叉树
    # left is smaller, right is larger !
    # in_order is sorted !

    def search(self, key, node=None):
        # 递归查找 key值为 key的节点并返回
        if node is None:
            node = self.root
        if node.key == key:
            return node
        if node.key > key:
            return self.search(key, node.left)
        return self.search(key, node.right)

    def search2(self, key, node=None):
        # 返回查找的最后节点
        if node is None:
            node = self.root
        while node.key:
            if node.key == key:
                return False
            elif node.key > key:
                if node.left is None:
                    return node
                else:
                    node = node.left
            elif node.key < key:
                if node.right is None:
                    return node
                else:
                    node = node.right
        return False

    def parent(self, key):
        parent = self.root
        node = parent
        if node.key == key:
            return False
        while node:
            if key > node.key:
                node = parent.right
            elif key < node.key:
                node = parent.left
            if key == node.key:
                return parent
            parent = node
        return False

    def insert(self, key):
        if not self.root.key:
            self.root.key = key
            return True
        rear = self.search2(key)
        if not rear:
            return False
        node = Node(key)
        if rear.key > key:
            rear.left = node
        elif rear.key < key:
            rear.right = node
        node.parent = rear

    def tree_max(self, node=None):
        # 返回树的最大元素
        if not node:
            node = self.root
        while node.right is not None:
            node = node.right
        return node

    def tree_min(self, node=None):
        # 返回树的最小元素
        if not node:
            node = self.root
        while node.left is not None:
            node = node.left
        return node

    def succ(self, key):
        # 前驱元素，为 y>x 的最小值
        node = self.search(key)
        if node.right is not None:
            return self.tree_min(node.right)
        parent = node.parent
        while parent is not None and parent.left != node:
            node = parent
            parent = parent.parent
        return parent

    def pred(self, key):
        # 后继元素，为 y<x 的最大值
        node = self.search(key)
        if node.left is not None:
            return self.tree_max(node.left)
        parent = node.parent
        while parent is not None and parent.right != node:
            node = parent
            parent = parent.parent
        return parent

    def delete(self, key):
        # 如果node没有子树，直接删node
        # 如果node只有一个子树，直接子树取代node
        # 如果node有两个子树，用右子树最小值取代node
        node = self.search(key)
        if node is None:
            return self.root
        old_node, parent = node, node.parent
        if node.right is None:
            node = node.left
        elif node.left is None:
            node = node.right
        else:
            y = self.tree_min(node.right)
            node.key = y.key
            if node.right == y:
                node.right = y.right
            else:
                y.parent.left = y.right
            return self.root
        if node is not None:
            node.parent = parent
        if parent is None:
            self.root = node
        else:
            if parent.left is old_node:
                parent.left = node
            else:
                parent.right = node
        return self.root

    def search_test(self, test_data=None, pr=False):
        # rand = [76, 47, 7, 37]
        self.__init__()
        if test_data is None:
            test_data = rand
        if pr:
            print test_data
        for i in test_data:
            self.insert(i)
        if pr:
            self.print_tree()
        node = self.rand_node()
        assert self.search(node.key) == node

        for smaller in self.in_order(node.left):
            assert smaller <= node.key
        for bigger in self.in_order(node.right):
            assert bigger >= node.key
            # self.print_tree()
            # self.pop(random.choice(test_data))
            # self.print_tree()


if __name__ == '__main__':
    bt = SearchTree()
    bt.search_test(pr=True)
