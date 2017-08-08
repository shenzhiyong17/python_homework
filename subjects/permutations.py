#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-03-17

def permutation(item, array):
    # 取一个数组的全排列，生成器版本
    if len(array) == 1:
        yield item + array
    else:
        for element in array:
            temp_list = array[:]
            temp_list.remove(element)
            for n in permutation(item + [element, ], temp_list):
                yield n


def permutation1(result, item, array):
    # 取一个数组的全排列，列表版本
    if len(array) == 1:
        result.append(item + tuple(array))
    else:
        for element in array:
            temp_list = array[:]
            temp_list.remove(element)
            permutation1(result, item + (element,), temp_list)
    return result


def combination(num, stat=()):
    # 返回长度为n 的全部组合
    if len(stat) == num:
        yield stat
    else:
        for r in 0, 1:
            for result in combination(num, stat + (r,)):
                yield result


if __name__ == '__main__':
    for item in permutation([], [1, 2, 3, 4]):
        print item
    print '=========='

    for item in permutation1([], (), [1, 2, 3, 4]):
        print item
    print '=========='

    for i in combination(4):
        print i
