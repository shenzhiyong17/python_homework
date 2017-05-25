#!/usr/bin/python
# -*- coding: utf-8 -*-
# 几何图形

import math


def san1(num=9):
    print 'san1:'
    for i in range(num):
        print '*' * (i + 1)


def san2(num=9):
    print 'san2:'
    for i in range(num):
        print ' ' * (num - i) + '*' * (i + 1)


def san3(num=9):
    print 'san3:'
    for i in range(num):
        j = num - i
        print '*' * j


def san4(num=9):
    print('san4:')
    for i in range(num):
        print(' ' * i + '*' * (num - i))


def san5(num=10):
    print('san5:')
    for i in range(1, num + 1):
        print(' ' * (num - i) + '*' * (2 * i - 1))


def san6(num=9):
    print('san6:')
    print(' ' * (num - 1) + '*')
    for i in range(2, num):
        front = (num - i)
        middle = (i * 2) - 3
        print(' ' * front + '*' + ' ' * middle + '*')
    print('* ' * (num))


def ling(num=10):
    san6(num)
    for i in range(1, num + 1):
        print(' ' * i + '*' * (2 * (num - i) - 1))


def su(num):
    if not isinstance(num, int):
        return str(num) + ' is not a int'
    elif num <= 1:
        return 'number must > 1'
    for i in range(2, int(num / 2 + 1)):
        if (num % i) == 0:
            print ' is not sushu'
    print str(num), " is sushu"
    return num


def psu(num):
    su = []
    for n in range(2, num + 1):
        for i in range(2, n):
            if (n % i) == 0:
                break
        su.append(n)
    print(su)


def sphere(R):
    times = 1
    for l in range(R):
        h = R - l
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        if r < 1:
            continue
        s = times * R - r
        # print '%2s' %(2 * r - 1),
        print('  ' * int(s) + '* ' * 2 * r)
    for h in range(1, R):
        l = R - h
        r = int(((R * R) - (h * h)) ** 0.5 * times)
        s = times * R - r
        # print '%2s' % (2 * r - 1),
        print('  ' * int(s) + '* ' * 2 * r)


def circle(R):
    times = 2
    for l in range(R):
        h = R - l
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        s = times * R - r
        #        space=str(' '*r+'$'*(r-2))
        space = str(' ' * (2 * r - 2))
        print(' ' * int(s) + '*' + space + '*')
    for h in range(R):
        l = R - h
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        s = times * R - r
        print(' ' * int(s) + '*' * 2 * r)


if __name__ == '__main__':
    # san1()
    # san2()
    # san3()
    # san4()
    # san5()
    # san6()
    # ling()
    sphere(10)
    # circle(20)
