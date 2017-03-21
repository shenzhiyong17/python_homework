#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from common.timing import timing
import prime


def factor(num):
    # 返回某数的因子
    sq = math.sqrt(num)
    lst = list([x for x in range(2, int(sq))])
    result = []
    while lst:
        i = lst[0]
        if num % i == 0:
            result.append(i)
            result.append(num / i)
        lst.remove(i)
    if sq % 1 == 0: result.append(int(sq))
    return sorted(result)

if __name__ == '__main__':
    print timing(factor, 20169985515)
