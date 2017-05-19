#!/usr/bin/python
# -*- coding: utf-8 -*-
# 从剩余元素中选择最大或最小的元素放在已排序列的最后

from dataStructure.common.test_data import rand


def select_sort(lst):
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst


def test(test_data):
    array = list(test_data)
    sort = select_sort(array)
    print 'rand: ', test_data
    print 'sort: ', sort
    assert sort == sorted(test_data)

if __name__ == '__main__':
    test(rand)
