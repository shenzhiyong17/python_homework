#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from common.timing import timing


def is_prime(num):
    # 判断num 是否质数
    for i in range(2, math.sqrt(num) + 1):
        if num % i == 0:
            return True
        return False


def primes(num):
    # 列出num 以内所有质数
    res = [1, ]
    for i in range(2, num + 1):
        mark = 0
        for j in res[1:]:
            if j <= math.sqrt(i) and i % j == 0:
                mark = 1
                break
        if mark == 0:
            res.append(i)
    return res


if __name__ == '__main__':
    print timing(primes, 2016)