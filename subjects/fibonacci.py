#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fib_r(num):
    # 斐波那契，递归版
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fib_r(num - 2) + fib_r(num - 1)


def fib_l(num):
    # 斐波那契，迭代版
    result = (0, 1)
    if num == 0 or num == 1:
        return result[num]
    else:
        for i in range(2, num + 1):
            result = (result[1], result[0] + result[1])
        return result[1]

if __name__ == '__main__':
    print fib_l(10)
    print fib_r(10)