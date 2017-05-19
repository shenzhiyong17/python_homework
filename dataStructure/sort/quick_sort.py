#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def quick1(array):
    if len(array) <= 1:
        return array
    p = array[0]
    left = filter(lambda x: x < p, array[1:])
    right = filter(lambda x: x >= p, array[1:])
    return quick1(left) + [p, ] + quick1(right)


def quick2(array, left=None, right=None):
    # 二路划分，不考虑元素相等的特殊情况
    if left is None:
        left = 0
    if right is None:
        right = len(array) - 1
    if left < right:
        i = left
        j = right
        p = array[left]
        while i < j:
            while array[j] > p and j > i:
                j -= 1
            array[i] = array[j]
            while array[i] <= p and i < j:
                i += 1
            array[j] = array[i]
        array[i] = p
        if i > left:
            quick2(array, left, i - 1)
        if j < right:
            quick2(array, j + 1, right)


def quick3(array, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(array) - 1
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
        quick3(array, left, j - 1)
        quick3(array, j + 1, right)


def quick4(array, left=0, right=None):
    # 三路划分，多数元素相等的情况下性能更好。
    pass


def test(test_data=rand):
    array1 = list(test_data)
    array2 = list(test_data)
    array3 = list(test_data)
    print test_data
    array1 = quick1(array1)
    print 'array1: ', array1
    quick2(array2, 0, len(array2) - 1)
    print 'array2: ', array2
    quick3(array3, 0, len(array3) - 1)
    print 'array3: ', array3
    print 'sorted: ', sorted(test_data)
    assert array1 == array2 == array3 == sorted(test_data)


if __name__ == '__main__':
    # test()
    quick4(rand)
