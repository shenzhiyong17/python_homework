#!/usr/bin/python

import random

import dataStructure.common.gen_rand
from dataStructure.sort.select_sort import select_sort


def bin_search(element, array, l, r):
    m = (l + r) / 2
    if element == array[m]:
        return m
    elif element > array[m]:
        return bin_search(element, array, m, r)
    elif element < array[m]:
        return bin_search(element, array, l, m)


def bin_search2(element, array):
    l = 0
    r = len(array)
    while l < r:
        m = (l + r) / 2
        if array[m] == element:
            return m
        elif array[m] < element:
            l = m + 1
        else:
            r = m
    return l


if __name__ == '__main__':
    for i in range(100):
        lst = select_sort(dataStructure.common.gen_rand.gen_rand_list(10))
        num = random.randint(0, 9)
        item = lst[num]
        print num, lst, item
        # print bin_search(item, lst, 0, len(lst) - 1)
        assert bin_search(item, lst, 0, len(lst)) == num
        assert bin_search2(item, lst) == num
