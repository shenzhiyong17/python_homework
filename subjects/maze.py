#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17

import random
import tools.colorFormat as colorFormat


def maze(h, v, p):  # 迷宫大小h x v. p为百分比.
    m = []
    for i in range(v):
        m.append([1, ] * h)
    for i in range(1, v - 1):
        for j in range(1, h - 1):
            if random.randint(0, 100) < p:
                m[i][j] = 0
    m[0][1] = m[v -1][h-2] = 0
    return m


def printm(maze):
    for line in maze:
        for item in line:
            if item == 0:
                item = colorFormat.color_format(item,mode='highlight')
            print item,
        print '\n'


if __name__ == '__main__':
    printm(maze(20, 10, 70))
