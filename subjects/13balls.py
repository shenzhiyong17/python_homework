#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-09-08

class Ball:
    _id = 0
    mark = None

    def __init__(self, weight=0):
        self.weight = weight
        self.id = self._id
        Ball._id += 1

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)

    def __int__(self):
        return self.weight

    def __str__(self):
        return 'ball %s weight: %s' % (self.id, self.weight)


def sum(array):
    res = 0
    for i in array:
        res += int(i)
    return res


def handle(balls):
    balls = list(balls)
    left = sum(balls[:4])  # 0, 1, 2, 3
    right = sum(balls[4:8])  # 4, 5, 6, 7
    if left == right:
        left = sum(balls[8:11])  # 8, 9, 10
        right = sum(balls[:3])  # 0, 1, 2
        if left == right:
            return balls[11] if balls[11] != balls[0] else balls[12]  # 11 / 12
        else:
            if balls[8] == balls[9]:
                return balls[10]  # 10
            elif balls[8] > balls[9]:
                return balls[8] if left > right else balls[9]  # 8 / 9
            else:
                return balls[9] if left > right else balls[8]  # 8 / 9
    else:
        if left < right:
            tmp = balls[:4]
            balls[:4] = balls[4:8]
            balls[4:8] = tmp
            # for b in balls:
            #     print b
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


if __name__ == '__main__':
    balls = [Ball() for i in range(13)]
    for i in range(13):
        print 'i: ', i
        balls[i].weight = 1
        print handle(balls)
        balls[i].weight = -1
        print handle(balls)
        balls[i].weight = 0
