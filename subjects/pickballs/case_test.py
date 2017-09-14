#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-09-08

from ball import *
import subjects.pickballs.nine_balls as handle_9
import subjects.pickballs.thirteen_balls as handle_13


def test(handle, num):
    print 'num: ', num, '----------------------'
    balls = [Ball(i) for i in range(num)]
    for i in range(num):
        print 'i: ', i
        balls[i].weight = 1
        b = handle(balls)
        print b
        balls[i].weight = -1
        b = handle(balls)
        print b
        balls[i].weight = 0


if __name__ == '__main__':
    test(handle_9.handle, 9)
    test(handle_13.handle, 13)
