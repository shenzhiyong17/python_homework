#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import dataStructure.tree.search_tree.avl as AVL
import dataStructure.tree.search_tree.rb_tree as RB
import dataStructure.tree.search_tree.search_tree as SearchTree
from common.timing import timing
from dataStructure.common.gen_rand import gen_rand_list
from dataStructure.sort.insert_sort import *
from dataStructure.sort.select_sort import *
from dataStructure.sort.merge_sort import *
from dataStructure.sort.quick_sort import *
from tools.output_format import output_format


class Performance:
    def __init__(self):
        pass

    @staticmethod
    def performance(*functions):
        output = output_format()
        title = ['data_len', ]
        for func in functions:
            title.append(func.__name__)
        output.addtest('performance', title)
        for data_len in (100, 300, 800, 5000):
            item = {'data_len': data_len}
            rand = gen_rand_list(data_len, 1, 9999)
            for func in functions:
                test_data = copy.deepcopy(rand)
                try:
                    time, res = timing(func, test_data)
                    item[func.__name__] = '%.3fms' % (time * 1000)
                except Exception as e:
                    print e
                    item[func.__name__] = 'fail'
            output.insert('performance', item)
        print output.gen_report()

    @staticmethod
    def search_tree():
        # insert and search and assert

        search = SearchTree.SearchTree()
        search = search.search_test

        avl = AVL.AVL()
        avl = avl.avl_test

        avl2 = AVL.AVL2()
        avl2 = avl2.avl2_test

        rb = RB.RBTree()
        rb = rb.rb_test

        Performance.performance(search, avl, avl2, rb)

    @staticmethod
    def sort():
        Performance.performance(select_sort, insert_sort1, insert_sort2, msort1, msort2, msort4, msort5, msort6, quick1, quick2, quick3)


if __name__ == '__main__':
    Performance.sort()
    Performance.search_tree()
