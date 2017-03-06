#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2016-2-3

from dataStructure.tree.binary_tree_by_linklist import BinaryTreeByLinkList

class Node():

    def __init__(self,key=None):
        self.key = key
        self.left = None
        self.left_thread = False
        self.right = None
        self.right_thread = False

class ThreadedTree(BinaryTreeByLinkList):
    root = Node()
    head = Node()

    def __init__(self,root=Node()):
        BinaryTreeByLinkList.__init__(self,root)
        self.root.left_thread = True
        self.root.right_thread = True
        self.root.right = self.head
        self.root.left = self.head
        self.head.left = self.root
        self.head.right = self.head


    def insucc(self,node):
        ### page 215 , 5-10
        temp = node.right
        if not node.right_thread :
            # print temp.key
            # print temp.left_thread
            while not temp.left_thread:
                temp = temp.left
                # print temp.key
                # print temp.left_thread
        return temp

    def in_order(self):
        temp = self.head
        res = []
        while True:
            temp = self.insucc(temp)
            if temp == self.head : break
            res.append(temp.key)
        return res

    def find(self,key):
        temp = self.head
        while True:
            temp = self.insucc(temp)
            if temp.key ==  key: break
        return temp

    def insert_right(self,parent,new):
        node = new
        node.right = parent.right
        node.right_thread = parent.right_thread
        node.left = parent
        node.left_thread = True
        parent.right = node
        parent.right_thread = False
        if not node.right_thread :
            temp = node.right
            temp.left = node

    def insert_left(self,parent,new):
        node = new
        node.left = parent.left
        node.left_thread = parent.left_thread
        node.right_thread = True
        node.right = parent
        parent.left_thread = False
        parent.left = node
        if not node.left_thread :
            temp = node.left
            temp.right = node

    def test(self):
        self.insert_right(self.root, Node('b'))
        parent = self.insucc(self.root)
        self.insert_right(self.root, Node('c'))
        parent = self.insucc(self.root)
        self.insert_left(self.root, Node('d'))
        parent = self.insucc(self.root)
        self.insert_left(self.root, Node('e'))
        parent = self.find('e')
        self.insert_right(parent, Node('f'))
        parent = self.find('c')
        self.insert_left(parent, Node('h'))
        print self.in_order()

if __name__ == '__main__':
    bt = ThreadedTree(Node('a'))
    bt.test()