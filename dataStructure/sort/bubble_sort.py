#!/usr/bin/python

import dataStructure.common.gen_rand as gen_rand


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

if __name__ == '__main__':
    array = gen_rand.gen_rand_list(15)
    print array
    print bubble_sort(array)
