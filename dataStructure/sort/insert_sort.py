#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def insert_sort1(array):
    for i in range(1, len(array)):
        x = array[i]
        j = i - 1
        while j >= 0 and array[j] > x:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = x
    return array


def insert_sort2(array):
    # 数组实现链表插入算法，对于A[i], next[i]存的是A[i]下一个元素的索引
    n = len(array)
    next_link = [-1, ] * (n + 1)
    for i in range(n):
        insert2(array, next_link, i)
        # print next_link
    # return next
    t = -1
    res = []
    while next_link[t] != -1:
        t = next_link[t]
        res.append(array[t])
    return res


def insert2(array, next_link, i):
    j = -1
    while next_link[j] != -1 and array[next_link[j]] < array[i]:
        j = next_link[j]
    next_link[j], next_link[i] = i, next_link[j]


def test(test_data):
    array1 = list(test_data)
    array2 = list(test_data)
    sort1 = insert_sort1(array1)
    sort2 = insert_sort2(array2)
    print 'rand:  ', test_data
    print 'sort1: ', sort1
    print 'sort2: ', sort2
    assert sort1 == sort2 == sorted(test_data)

if __name__ == '__main__':
    test(rand)


