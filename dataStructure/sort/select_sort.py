#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def select_sort(lst):
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst


if __name__ == '__main__':
    array = list(rand)
    sort = select_sort(array)
    print 'rand: ', rand
    print 'sort: ', sort
    assert sort == sorted(rand)
