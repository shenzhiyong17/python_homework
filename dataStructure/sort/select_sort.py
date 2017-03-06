#!/usr/bin/python

import dataStructure.common.gen_rand as gen_rand

def select_sort(lst):
    for i in range(len(lst)-1):
        for j in range(i+1, len(lst)):
            if lst[i] > lst[j]:
                lst[i],lst[j] = lst[j],lst[i]
    return lst


if __name__ == '__main__':
    array = gen_rand.gen_rand_list(15)
    print array
    print select_sort(array)