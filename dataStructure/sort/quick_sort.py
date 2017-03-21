#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def quick1(array, left, right):
    if left < right:
        i = left
        j = right
        p = array[left]
        while i < j:
            i += 1
            while array[i] < p and i < len(array) - 1:
                i += 1
            while array[j] > p:
                j -= 1
            if i < j:
                array[i], array[j] = array[j], array[i]
        array[left], array[j] = array[j], array[left]
        quick1(array, left, j - 1)
        quick1(array, j + 1, right)


def quick2(array, left, right):
    if left < right:
        i = left
        j = right
        p = array[left]
        while i < j:
            while (array[j] > p and j > i):
                j -= 1
            array[i] = array[j]
            while (array[i] <= p and i < j):
                i += 1
            array[j] = array[i]
        array[i] = p
        if i > left:
            quick2(array, left, i - 1)
        if j < right:
            quick2(array, j + 1, right)


def quick3(arrary):
    if len(arrary) <= 1:
        return arrary
    p = arrary[0]
    left = filter(lambda x: x < p, arrary[1:])
    right = filter(lambda x: x >= p, arrary[1:])
    return quick3(left) + [p, ] + quick3(right)


def test(randlist=rand):
    array1 = list(randlist)
    array2 = list(randlist)
    array3 = list(randlist)
    print randlist
    quick1(array1, 0, len(array1) - 1)
    print 'array1: ', array1
    quick2(array2, 0, len(array2) - 1)
    print 'array2: ', array2
    array3 = quick3(array3)
    print 'array3: ', array3
    print 'sorted: ', sorted(randlist)
    assert array1 == array2 == array3 == sorted(randlist)


if __name__ == '__main__':
    test(rand)
