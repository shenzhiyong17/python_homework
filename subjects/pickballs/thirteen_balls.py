#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-09-08

# 3层3叉树（=,>,<），共27个末端节点，能得出27个解
# 13×2 = 26，共26个可能性
# 2x8=16, 3**2x2=18, 表示3叉树末端不能被完全利用
# 5x2=10, 3**2=9, 表示3叉树末端不够分，少一个节点，表示最终有一个小球能被挑出来但不知轻重

from ball import *


def handle(balls):
    balls = list(balls)
    left = sum(balls[:4])  # 0, 1, 2, 3
    right = sum(balls[4:8])  # 4, 5, 6, 7
    if left == right:
        left = sum(balls[8:10])  # 8, 9
        right = sum([balls[10], balls[0]])  # 0, 10
        if left == right:  # 11, 12
            if balls[11] == balls[0]:
                return balls[12]
            elif balls[11] > balls[0]:
                balls[11].mark = 1
                return balls[11]
            else:
                balls[11].mark = -1
                return balls[11]
        else:  # 8, 9, 10
            if left > right:
                balls[8].mark = 1
                balls[9].mark = 1
                balls[10].mark = -1
            else:
                balls[8].mark = -1
                balls[9].mark = -1
                balls[10].mark = 1
            if balls[8] == balls[9]:
                return balls[10]
            elif balls[8] > balls[9]:
                return balls[8] if left > right else balls[9]
            else:
                return balls[9] if left > right else balls[8]
    else:
        if left < right:
            tmp = balls[:4]
            balls[:4] = balls[4:8]
            balls[4:8] = tmp
        for b in balls[:4]:
            b.mark = 1
        for b in balls[4:8]:
            b.mark = -1
        left = sum(balls[:3] + balls[4:6])  # 0, 1, 2, 4, 5
        right = sum(balls[8:])  # 8, 9, 10, 11, 12
        if left == right:  # 3, 6, 7
            left = sum([balls[3]] + [balls[6]])
            right = sum(balls[:2])
            if left == right:
                return balls[7]  # 7
            elif left > right:
                return balls[3]
            else:
                return balls[6]
        elif left > right:  # 0, 1, 2
            left = balls[0]
            right = balls[1]
            if left == right:
                return balls[2]
            elif left > right:
                return balls[0]
            else:
                return balls[1]
        else:  # 4, 5
            return balls[4] if balls[4] < balls[5] else balls[5]
