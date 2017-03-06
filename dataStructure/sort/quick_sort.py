#!/usr/bin/python

import dataStructure.common.gen_rand as gen_rand


def quick(ls, left, right):
    if left < right:
        i = left
        j = right
        print ls
        p = ls[left]
        while i < j:
            i += 1
            while ls[i] < p and i < len(ls) - 1:
                i += 1
            while ls[j] > p:
                j -= 1
            if i < j:
                ls[i], ls[j] = ls[j], ls[i]
        ls[left] = ls[j]
        ls[j] = p
        quick(ls, left, j - 1)
        quick(ls, j + 1, right)


def quick1(array, begin, end):
    if begin > end: return
    print array
    i = begin
    j = end
    p = array[begin]
    while i < j:
        while (array[j] > p and j > i):
            j -= 1
        array[i] = array[j]
        while (array[i] <= p and i < j):
            i += 1
        array[j] = array[i]
    array[i] = p
    if i > begin:
        quick1(array, begin, i - 1)
    if j < end:
        quick1(array, j+1, end)


if __name__ == '__main__':
    # ls = [7, 6, 5, 4, 32, 1]
    ls = gen_rand.gen_rand_list(10, 0, 99)
    ls = [98, 12, 16, 52, 85, 50, 71, 44, 25, 29]
    quick1(ls, 0, len(ls) - 1)
    print ls
