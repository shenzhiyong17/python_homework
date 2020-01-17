#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-01-22

import unittest

import data_structure.basic.single_link_list as SingleLink
import data_structure.sort.bubble_sort as BubbleSort
import data_structure.sort.select_sort as SelectSort
import data_structure.sort.insert_sort as InsertSort
import data_structure.sort.merge_sort as MergeSort
import data_structure.sort.quick_sort as QuickSort
import data_structure.tree.binary_tree_by_arrary as BinTreeByArray
import data_structure.tree.completely_tree as CompletelyTree
import data_structure.tree.heap.deap as Deap
import data_structure.tree.heap.leftist as Leftist
import data_structure.tree.heap.max_heap as MaxHeap
import data_structure.tree.heap.min_max_heap as MinMaxHeap
import data_structure.tree.radix_tree.int_patricia as IntPatricia
import data_structure.tree.radix_tree.int_trie as IntTrie
import data_structure.tree.search_tree.avl as AVL
import data_structure.tree.search_tree.rb_tree as RBTree
import data_structure.tree.search_tree.search_tree as SearchTree
import data_structure.tree.threaded_tree as ThreadTree
from data_structure.common.test_data import rand
import data_structure.sort.championship_tree as ChampionTree
import data_structure.tree.heap.Heapify as Heapify


class TestCase(unittest.TestCase):

    def test_insert_sort(self):
        test = InsertSort.test
        test(rand)

    def test_bubble_sort(self):
        test = BubbleSort.test
        test(rand)

    def test_select_sort(self):
        test = SelectSort.test
        test(rand)

    def test_merge_sort(self):
        test = MergeSort.test
        test(rand)

    def test_quick_sort(self):
        test = QuickSort.test
        test(rand)

    def test_single_link(self):
        link = SingleLink.LinkList()
        link.test()

    def test_bin_tree_by_array(self):
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
        tree.search_test()

    def test_rb_tree(self):
        tree = RBTree.RBTree()
        tree.rb_test()

    def test_avl_tree(self):
        tree = AVL.AVL()
        tree.avl_test()

    def test_avl2_tree(self):
        tree = AVL.AVL2()
        tree.avl2_test()

    def test_trie(self):
        tree = IntTrie.IntTrie()
        tree.test()

    def test_int_patricia(self):
        tree = IntPatricia.IntPatricia()
        tree.test()

    def test_deep(self):
        heap = Deap.Deap()
        heap.deap_test()

    def test_maxheap(self):
        heap = MaxHeap.MaxHeap()
        heap.max_heap_test()

    def test_heapify(self):
        heap = Heapify.Heapify()
        heap.heapify_test()

    def test_leftist(self):
        heap = Leftist.Leftist()
        heap.leftist_test()

    def test_min_max_heap(self):
        heap = MinMaxHeap.MinMaxHeap()
        heap.min_max_heap_test()

    def test_champion_tree(self):
        ct = ChampionTree.ChampionTree()
        ct.test()


if __name__ == "__main__":
    unittest.main()
