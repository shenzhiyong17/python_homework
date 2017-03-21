#!/usr/bin/python

from dataStructure.common.test_data import rand


def bubble_sort(array):
    for i in range(0, len(array) - 1):
        j = i + 1
        while array[j] < array[j - 1] and j >= 1:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1
    return array


def wrong_sort(array):
    for i in range(0, len(array)-1):
        for j in range(0,i+1):
            if array[j] < array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

    return array

def test(rand):
    array = list(rand)
    sort = bubble_sort(array)
    print 'rand:  ', rand
    print 'sort:  ', sort
    assert sort == sorted(rand)

if __name__ == '__main__':
    test(rand)
