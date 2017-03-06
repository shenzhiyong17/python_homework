#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-1-18

import dataStructure.common.node as BasicNode
from common.Enum import Enum
from dataStructure.common.test_data import rand
from dataStructure.tree.binary_tree_by_linklist import BinaryTreeByLinkList

Color = Enum(("RED", "BLACK"))


class RBTree(BinaryTreeByLinkList):
    # 红黑树，from《算法新解》，旋转后返回根节点，或者不返回
    # 1，节点要么红色，要么黑色
    # 2，根节点为黑色
    # 3，所有叶子节点（占位空节点）为黑色
    # 4，如果一个节点为红色，它的两个子节点都为黑色
    # 5，对任一节点，从它出发到所有叶子节点的路经上包含相同数量的黑色节点

    class Node(BasicNode.Node):

        def __init__(self, key=None, parent=None):
            BasicNode.Node.__init__(self, key)
            self.color = Color.BLACK
            self.parent = parent

        def __str__(self):
            return '%s（%s）' % (self.key, self.color)

    def __init__(self, root=None):
        self.root = self.creat_node(root)

    def creat_node(self, key):
        node = self.Node(key)
        node.color = Color.RED
        node.left = self.Node(parent=node)
        node.right = self.Node(parent=node)
        return node

    def isEmpty(self, node):
        return node.key is None

    def insert(self, key):
        t = self.root
        x = self.creat_node(key)
        parent = None
        while t.key:
            parent = t
            if x > t:
                t = t.right
            elif x < t:
                t = t.left
            else:
                return self.root
        if parent is None:
            self.root = x
        elif x < parent:
            parent.left = x
            x.parent = parent
        else:
            parent.right = x
            x.parent = parent
        return self.insert_fix(x)

    def uncle(self, node):
        if self.grandparent(node) is None:
            return None
        parent = node.parent
        grandparent = self.grandparent(node)
        if parent < grandparent:
            if grandparent.right is None:
                grandparent.right = self.Node(parent=grandparent)
            uncle = grandparent.right
        else:
            if grandparent.left is None:
                grandparent.left = self.Node(parent=grandparent)
            uncle = grandparent.left
        return uncle

    def grandparent(self, node):
        try:
            return node.parent.parent
        except Exception:
            return None

    def left_rotate(self, node):
        # 左旋时node为最小值
        # self.print_tree()
        if node.right.right:
            # print 'left_rotate 2 %s' % node
            y = node.right
            y.parent = node.parent
            node.parent = y
            node.right = y.left
            node.right.parent = node
            y.left = node
        else:
            # print 'left_rotate 4 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.right = y.left
            node.right.parent = node
            y.left = node
        if y.parent is None:
            self.root = y
        elif y.parent < y:
            y.parent.right = y
        else:
            y.parent.left = y
        # self.print_tree()

    def right_rotate(self, node):
        # 右旋时node为最小值
        # self.print_tree()
        if node.left.left:
            # print 'right_rotate 1 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.left = y.right
            node.left.parent = node
            y.right = node
        else:
            # print 'right_rotate 3 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.left = y.right
            node.left.parent = node
            y.right = node
        if y.parent is None:
            self.root = y
        elif y.parent > y:
            y.parent.left = y
        else:
            y.parent.right = y
        # self.print_tree()

    def insert_fix(self, node):  # 六种情况下需要调节节点颜色，然后通过左右旋保持平衡
        # print 'insert_fix %s\t\t' % node,
        # print 'node.parent: %s' % node.parent
        while (node.parent and node.parent.color == Color.RED):
            # print 'node %s' % node
            # print 'uncle: %s' % self.uncle(node)
            if self.uncle(node).color == Color.RED:
                # print 'uncle.color == Color.RED',
                node.parent.color = Color.BLACK
                self.grandparent(node).color = Color.RED
                self.uncle(node).color = Color.BLACK
                # print '%s -> BLACK, %s -> RED, %s -> BLACK' % (node.parent, self.grandparent(node), self.uncle(node))
                node = self.grandparent(node)
            else:
                # print 'uncle.color == Color.BLACK'
                if node.parent == self.grandparent(node).left:
                    if node == node.parent.right:
                        node = node.parent
                        # print 'node: %s ...' % node
                        self.left_rotate(node)
                    node.parent.color = Color.BLACK
                    self.grandparent(node).color = Color.RED
                    self.right_rotate(self.grandparent(node))
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = Color.BLACK
                    # print 'grandparent: %s' % self.grandparent(node)
                    self.grandparent(node).color = Color.RED
                    self.left_rotate(self.grandparent(node))
        self.root.color = Color.BLACK
        return self.root

    def test(self):
        # rand = [70, 84, 62, 89, 49, 62, 25, 96, 68, 73]
        print rand
        for i in rand:
            self.insert(i)
        pre = self.pre_order(self.root)
        print '==============================================='
        self.print_tree()

if __name__ == '__main__':
    bt = RBTree()
    bt.test()
