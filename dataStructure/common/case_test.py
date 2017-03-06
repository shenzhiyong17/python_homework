#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-01-22

import unittest

import dataStructure.basic.single_link_list as SingleLink
import dataStructure.tree.binary_tree_by_arrary as BinTreeByArray
import dataStructure.tree.completely_tree as CompletelyTree
import dataStructure.tree.radix_tree.int_patricia as IntPatricia
import dataStructure.tree.radix_tree.int_trie as IntTrie
import dataStructure.tree.search_tree.avl as AVL
import dataStructure.tree.search_tree.rb_tree as RBTree
import dataStructure.tree.search_tree.search_tree as SearchTree
import dataStructure.tree.threaded_tree as ThreadTree


class TestCase(unittest.TestCase):

    def test_single_link(self):
        link = SingleLink.LinkList()
        link.test()

    def test_bin_tree_by_arrary(self):
        tree = BinTreeByArray.BinaryTreeByArray()
        tree.test()

    def test_completely_tree(self):
        tree = CompletelyTree.CompletelyTree()
        tree.test()

    def test_thread_tree(self):
        tree = ThreadTree.ThreadedTree()
        tree.test()

    def test_search_tree(self):
        tree = SearchTree.SearchTree()
        tree.test()

    def test_rb_tree(self):
        tree = RBTree.RBTree()
        tree.test()

    def test_avl_tree(self):
        tree = AVL.AVL()
        tree.test()

    def test_avl2_tree(self):
        tree = AVL.AVL2()
        tree.test()

    def test_trie(self):
        tree = IntTrie.IntTrie()
        tree.test()

    def test_int_patricia(self):
        tree = IntPatricia.IntPatricia()
        tree.test()

if __name__ == "__main__":
    unittest.main()
