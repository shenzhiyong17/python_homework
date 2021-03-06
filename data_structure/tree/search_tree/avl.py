#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-19

import random

import data_structure.tree.node as BasicNode
from data_structure.common.test_data import rand
from data_structure.tree.binary_tree_by_linklist import BinaryTreeByLinkList


class AVL(BinaryTreeByLinkList):
    # 平衡查找树，左小右大
    # 通过左右旋转保持查找数的二叉平衡性。
    # from《数据结构》，node没有parent指针，旋转要注意原地返回
    # 递归 insert
    unbalanced = False

    class Node(BasicNode.Node):
        def __init__(self, key=None):
            BasicNode.Node.__init__(self, key)
            self.bf = 0         # 平衡因子，bf = Hl-Hr，取值 [-1,0,1]

        def __str__(self):
            return '%s.%s' % (self.key, self.bf)

    def __init__(self, root_key=None):
        BinaryTreeByLinkList.__init__(self, self.Node(root_key))

    def insert(self, root, key):
        if root is self.root and self.root.key is None:
            root = self.Node(key)
            self.unbalanced = False
        elif not root:
            root = self.Node(key)
            self.unbalanced = True
        elif key < root.key:
            root.left = self.insert(root.left, key)
            if self.unbalanced:
                if root.bf == -1:
                    root.bf = 0
                    self.unbalanced = False
                elif root.bf == 0:
                    root.bf = 1
                elif root.bf == 1:
                    root = self.right_rotation(root)
                else:
                    raise
        elif key > root.key:
            root.right = self.insert(root.right, key)
            if self.unbalanced:
                if root.bf == 1:
                    root.bf = 0
                    self.unbalanced = False
                elif root.bf == 0:
                    root.bf = -1
                elif root.bf == -1:
                    root = self.left_rotation(root)
                else:
                    raise
        else:
            self.unbalanced = False
            # print "%s is already in the tree." % key
        return root

    def right_rotation(self, root):
        child = root.left
        if child.bf == 1:
            # LL rotation
            # 新节点在root的左子树的左子树下，root为最靠下的bf为正负2的节点
            root.left = child.right
            child.right = root
            root.bf = 0
            root = child
        else:
            # LR rotation
            # 新节点在root的左子树的右子树下
            grand_child = child.right
            child.right = grand_child.left
            grand_child.left = child
            root.left = grand_child.right
            grand_child.right = root
            if grand_child.bf == 1:
                root.bf = -1
                child.bf = 0
            elif grand_child.bf == 0:
                root.bf = 0
                child.bf = 0
            elif grand_child.bf == -1:
                root.bf = 0
                child.bf = 1
            else:
                raise
            root = grand_child
        root.bf = 0
        self.unbalanced = False
        return root

    def left_rotation(self, root):
        child = root.right
        if child.bf == -1:
            root.right = child.left
            child.left = root
            root.bf = 0
            root = child
        else:
            # LR rotation
            grand_child = child.left
            child.left = grand_child.right
            grand_child.right = child
            root.right = grand_child.left
            grand_child.left = root
            if grand_child.bf == 1:
                root.bf = -1
                child.bf = 0
            elif grand_child.bf == 0:
                root.bf = 0
                child.bf = 0
            elif grand_child.bf == -1:
                root.bf = 0
                child.bf = 1
            else:
                raise
            root = grand_child
        root.bf = 0
        self.unbalanced = False
        return root

    def search(self, key):
        node = self.root
        while node is not None and node.key != key:
            if node.key > key:
                node = node.left
            else:
                node = node.right
        if node:
            return node
        raise

    def avl_test(self, test_data=None, pr=False):
        self.__init__()
        # rand = [70, 45, 72, 36, 83, 93, 82, 8, 99, 36, 65, 56, 5, 8, 86, 31, 4, 72, 47, 52]
        if test_data is None:
            test_data = rand
        if pr:
            print test_data
        for i in test_data:
            self.root = self.insert(self.root, i)
        if pr:
            self.print_tree()
        rand_key = random.choice(test_data)
        node = self.search(rand_key)
        assert node.key == rand_key

        for smaller in self.in_order(node.left):
            assert smaller <= node.key
        for bigger in self.in_order(node.right):
            assert bigger >= node.key


class AVL2(BinaryTreeByLinkList):
    # from《算法新解》，insert用从下到上的迭代，左右旋转同红黑树
    # bf 设置与 上边 相反
    class Node(BasicNode.Node):
        def __init__(self, key=None, parent=None):
            BasicNode.Node.__init__(self, key)
            self.bf = 0          # 平衡因子，bf = Hr-Hl，取值 [-1,0,1]
            self.parent = parent

        def __str__(self):
            return '%s.%s' % (self.key, self.bf)

    def __init__(self, root_key=None):
        BinaryTreeByLinkList.__init__(self, self.create_node(root_key))

    def create_node(self, key):
        node = self.Node(key)
        node.left = self.Node(parent=node)
        node.right = self.Node(parent=node)
        return node

    def insert(self, key):
        x = self.create_node(key)
        parent = None
        t = self.root
        while t.key:
            parent = t
            if x > t:
                t = t.right
            elif x < t:
                t = t.left
            else:
                # print '%s is already in tree' % key
                return
        if parent is None:
            self.root = x
        elif x > parent:
            parent.set_right(x)
        else:
            parent.set_left(x)
        x.parent = parent
        self.insert_fix(x)

    def insert_fix(self, node):
        while node.parent is not None:
            bf = node.parent.bf
            if node is node.parent.left:
                bf -= 1
            else:
                bf += 1
            node.parent.bf = bf
            (l, p, r) = (node.parent.left, node.parent, node.parent.right)
            if abs(bf) == 0:
                return
            elif abs(bf) == 1:
                node = node.parent
            elif abs(bf) == 2:
                if bf == 2:
                    if r.bf == 1:  # RR偏
                        p.bf = 0
                        r.bf = 0
                        self.left_rotate(p)
                    elif r.bf == -1:  # RL偏
                        dy = r.left.bf
                        if dy == 1:
                            p.bf = -1
                        else:
                            p.bf = 0
                        r.left.bf = 0
                        if dy == -1:
                            r.bf = 1
                        else:
                            r.bf = 0
                        self.right_rotate(r)
                        self.left_rotate(p)
                elif bf == -2:
                    if l.bf == -1:  # LL偏
                        p.bf = 0
                        l.bf = 0
                        self.right_rotate(p)
                    elif l.bf == 1:  # LR偏
                        dy = l.right.bf
                        if dy == 1:
                            l.bf = -1
                        else:
                            l.bf = 0
                        l.right.bf = 0
                        if dy == -1:
                            p.bf = 1
                        else:
                            p.bf = 0
                        self.left_rotate(l)
                        self.right_rotate(p)
                break

    def left_rotate(self, node):
        # 左旋时node为最小值
        if node.right.right:
            # print 'left_rotate 2 %s' % node
            y = node.right
            y.parent = node.parent
            node.parent = y
            node.set_right(y.left)
            y.left = node
        else:
            # print 'left_rotate 4 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.set_right(y.left)
            y.left = node
        if y.parent is None:
            self.root = y
        elif y.parent < y:
            y.parent.right = y
        else:
            y.parent.left = y

    def right_rotate(self, node):
        # 右旋时node为最小值
        if node.left.left:
            # print 'right_rotate 1 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.set_left(y.right)
            y.right = node
        else:
            # print 'right_rotate 3 %s' % node
            y = node.left
            y.parent = node.parent
            node.parent = y
            node.set_left(y.right)
            y.right = node
        if y.parent is None:
            self.root = y
        elif y.parent > y:
            y.parent.left = y
        else:
            y.parent.right = y

    def search(self, key):
        node = self.root
        while node is not None and node.key != key:
            if node.key > key:
                node = node.left
            else:
                node = node.right
        if node:
            return node
        raise

    def avl2_test(self, test_data=None, pr=False):
        self.__init__()
        # rand = [27, 30, 10, 86, 47, 36, 7, 2, 84, 80, 68, 65, 35, 82, 85, 51, 99, 86, 93, 62]
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


if __name__ == '__main__':
    avl = AVL()
    avl.avl_test(pr=True)

    avl = AVL2()
    avl.avl2_test(pr=True)
