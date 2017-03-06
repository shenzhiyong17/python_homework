#!/usr/bin/python

import sys


def merge(ls, start, mid, end):
    left = ls[start:mid + 1]
    right = ls[mid + 1:end + 1]
    print 'left: ', left
    print 'right: ', right

    i = 0
    j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            ls[k] = left[i]
            i += 1
            k += 1
        elif left[i] > right[j]:
            ls[k] = right[j]
            j += 1
            k += 1
    while i < len(left):
        ls[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        ls[k] = right[j]
        j += 1
        k += 1


def sort(ls, start, end):
    if start < end:
        mid = (start + end) / 2
        sort(ls, start, mid)
        sort(ls, mid + 1, end)
        merge(ls, start, mid, end)


if __name__ == '__main__':
    ls = [8, 6, 5, 4, 1, 2, 7, 9]
    # ls = sys.argv[1:]
    print ls
    sort(ls, 0, len(ls) - 1)
    print ls
