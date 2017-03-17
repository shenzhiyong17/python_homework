#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-03-17

def permutation(item, array):
    """
        取一个数组的全排列
        array：为输入列表
        item：中间结果
    """
    # 生成器版本
    if len(array) == 1:
        yield item + array
    else:
        for element in array:
            temp_list = array[:]
            temp_list.remove(element)
            for n in permutation(item + [element, ], temp_list):
                yield n


def permutation1(result, item, array):
    # result：结果列表
    # 列表版本
    if len(array) == 1:
        result.append(item + array)
    else:
        for element in array:
            temp_list = array[:]
            temp_list.remove(element)
            permutation1(result, item + [element, ], temp_list)
    return result


for item in permutation([], [1, 2, 3, 4]):
    print item

for item in permutation1([], [], [1, 2, 3, 4]):
    print item
