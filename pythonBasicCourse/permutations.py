#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-03-17

def permutation(result, item, array):
    """
        取一个数组的全排列
        array：为输入列表
        item：中间结果
        result： 为结果列表
    """
    if len(array) == 1:
        result.append(item + array)
    else:
        for element in array:
            temp_list = array[:]
            temp_list.remove(element)
            permutation(result, item + [element, ], temp_list)
    return result


for item in permutation([], [], [1, 2, 3, 4]):
    print item
