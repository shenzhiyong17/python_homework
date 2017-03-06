#!/usr/bin/python

import random

import dataStructure.common.gen_rand
from dataStructure.sort.select_sort import select_sort


def binsearch(item, lst, l, r):
    m = (l + r ) / 2
    if item == lst[m]:
        return m
    elif item > lst[m]:
        return binsearch(item, lst, m, r)
    elif item < lst[m]:
        return binsearch(item, lst, l, m)

def binsearch2(item, lst):
    l = 0
    r = len(lst)
    while l < r:
        m = (l + r) / 2
        if lst[m] == item:
            return m
        elif lst[m] < item:
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
        # print binsearch(item, lst, 0, len(lst) - 1)
        assert binsearch(item, lst, 0, len(lst)) == num
        assert binsearch2(item, lst) == num
