#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt


def factor(num):
    # 返回某数的因子
    sq = sqrt(num)
    lst = list([x for x in range(2, int(sq))])
    result = []
    while lst:
        i = lst[0]
        if num % i == 0:
            result.append(i)
            result.append(num / i)
        lst.remove(i)
    if sq % 1 == 0: result.append(int(sq))
    return result

if __name__ == '__main__':
    print factor(2016)