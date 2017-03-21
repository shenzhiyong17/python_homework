#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.common.test_data import rand


def merge(array, start, mid, end):
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


def sort(array, start=0, end=-1):
    if end == -1:
        end = len(array) - 1
    if start < end:
        mid = (start + end) / 2
        sort(array, start, mid)
        sort(array, mid + 1, end)
        merge(array, start, mid, end)


def test(randlist=rand):
    array = list(randlist)
    print 'rand:   ', randlist
    sort(array)
    print 'array:  ', array
    print 'sorted: ', sorted(randlist)
    assert array == sorted(randlist)


if __name__ == '__main__':
    test(rand)
