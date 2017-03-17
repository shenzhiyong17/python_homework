#!/usr/bin/env python
# -*- coding: utf-8 -*-


def factorial(num):
    # 返回 n的阶乘，递归版
    if num <= 1:
        return 1
    else:
        return num * factorial(num - 1)


def factorial_l(num):
    # 返回 n的阶乘，迭代版
    result = 1
    if not num <= 1:
        for i in range(1, num + 1):
            result *= i
    return result

if __name__ == '__main__':
    print factorial(5)
    print factorial_l(5)