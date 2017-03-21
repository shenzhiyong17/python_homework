#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand

def insert_sort1(A):
    for i in range(1, len(A)):
        x = A[i]
        j = i - 1
        while j >= 0 and A[j] > x:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = x
    return A


def insert_sort2(A):
    ## 数组实现链表插入算法，对于A[i], next[i]存的是A[i]下一个元素的索引
    n = len(A)
    next = [-1, ] * (n + 1)
    for i in range(n):
        insert2(A, next, i)
    # return next
    t = -1
    res = []
    while next[t] != -1:
        t = next[t]
        res.append(A[t])
    return res


def insert2(A, next, i):
    j = -1
    while next[j] != -1 and A[next[j]] < A[i]:
        j = next[j]
    next[j], next[i] = i, next[j]

def test(rand):
    array1 = list(rand)
    array2 = list(rand)
    sort1 = insert_sort1(array1)
    sort2 = insert_sort1(array2)
    print 'rand:  ', rand
    print 'sort1: ', sort1
    print 'sort2: ', sort2
    assert sort1 == sort2 == sorted(rand)

if __name__ == '__main__':
    test(rand)


