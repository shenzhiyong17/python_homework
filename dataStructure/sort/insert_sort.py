#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
    while next[t] != -1:
        t = next[t]
        print A[t],


def insert2(A, next, i):
    j = -1
    while next[j] != -1 and A[next[j]] < A[i]:
        j = next[j]
    next[j], next[i] = i, next[j]


if __name__ == '__main__':
    from dataStructure.common import gen_rand

    rand = gen_rand.gen_rand_list(6, 1, 99)
    # rand = [76, 47, 7, 37]
    print rand
    insert_sort2(rand)
