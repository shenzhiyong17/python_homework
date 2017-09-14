#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-09-08

# 第一层   3：3：3
# 第二层   2：1 + 2：1 + 2：1


from subjects.pickballs.ball import *


def handle(balls):
    balls = list(balls)
    normal = []
    left = sum(balls[:3])  # 0, 1, 2
    right = sum(balls[3:6])  # 3, 4, 5
    if left == right:  # 6, 7, 8
        normal.extend(balls[:6])
        left = sum(balls[6:8])  # 6, 7
        right = sum([normal[0], balls[8]])  # 0, 8
        if left > right:
            balls[6].mark = 1
            balls[7].mark = 1
            balls[8].mark = -1
            if balls[6] == balls[7]:
                return balls[8]
            else:
                return balls[6] if balls[6] > balls[7] else balls[7]
        else:
            balls[6].mark = -1
            balls[7].mark = -1
            balls[8].mark = 1
            if balls[6] == balls[7]:
                return balls[8]
            else:
                return balls[6] if balls[6] < balls[7] else balls[7]
    else:
        normal.extend(balls[6:])
        if left < right:  # interchange
            tmp = balls[:3]
            balls[:3] = balls[3:6]
            balls[3:6] = tmp
        for b in balls[:3]:
            b.mark = 1
        for b in balls[3:6]:
            b.mark = -1
        left = sum(balls[:2] + balls[3:4])  # 0, 1, 3
        right = sum(normal[:3])  # 6, 7, 8
        if left == right:  # 2, 4, 5
            if balls[4] == balls[5]:
                return balls[2]
            else:
                return balls[4] if balls[4] < balls[5] else balls[5]
        elif left > right:  # 0, 1
            return balls[0] if balls[0] > balls[1] else balls[1]
        else:  # 3
            return balls[3]
