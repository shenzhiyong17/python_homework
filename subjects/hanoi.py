#!/usr/bin/env python
# -*- coding: utf-8 -*-


def hanoi(num, a, b, c):
    # 汉诺塔
    if num == 1:
        print '%-3s,%s -> %s' % (num * '-', a, c)
    else:
        hanoi(num - 1, a, c, b)
        print '%-3s,%s -> %s' % (num * '-', a, c)
        hanoi(num - 1, b, a, c)


if __name__ == '__main__':
    hanoi(5, 'a', 'b', 'c')
