#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def merge1(array, start, mid, end):
    left = array[start:mid + 1]
    right = array[mid + 1:end + 1]
    i = 0
    j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        array[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        array[k] = right[j]
        j += 1
        k += 1


def msort1(array, start=0, end=-1):
    if end == -1:
        end = len(array) - 1
    if start < end:
        mid = (start + end) / 2
        msort1(array, start, mid)
        msort1(array, mid + 1, end)
        merge1(array, start, mid, end)


def merge2(array, left, right):
    # 简洁版
    i = 0
    while left != [] and right != []:
        array[i] = left.pop(0) if left[0] < right[0] else right.pop(0)
        i += 1
    array[i:] = left if left != [] else right


def msort2(array):
    # 简洁版
    n = len(array)
    if n > 1:
        left = [x for x in array[:n / 2]]
        right = [x for x in array[n / 2:]]
        left = msort2(left)
        right = msort2(right)
        merge2(array, left, right)
    return array


def test(randlist=rand):
    array1 = list(randlist)
    array2 = list(randlist)
    print 'rand:    ', randlist
    msort1(array1)
    print 'array1:  ', array1
    array2 = msort2(array2)
    print 'array2:  ', array2
    print 'sorted:  ', sorted(randlist)
    assert array1 == array2 == sorted(randlist)


if __name__ == '__main__':
    test(rand)
