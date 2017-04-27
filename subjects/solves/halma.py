#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-26
# Halma(跳棋), 求跳蛙/单人跳棋 的解


class Halma():
    def __init__(self, size):
        # -1 的棋只能往右, 1 的棋只能往左, 0 为空
        self.start = [-1] * size + [0] + [1] * size
        self.end = [1] * size + [0] + [-1] * size

    def moves(self, s):
        # 可能的动作
        ms = []
        n = len(s)
        p = s.index(0)
        if p < n - 2 and s[p + 2] == 1:
            ms.append(self.swap(s, p, p + 2))
        if p < n - 1 and s[p + 1] == 1:
            ms.append(self.swap(s, p, p + 1))
        if p > 1 and s[p - 2] == -1:
            ms.append(self.swap(s, p, p - 2))
        if p > 0 and s[p - 1] == -1:
            ms.append(self.swap(s, p, p - 1))
        return ms

    def swap(self, s, i, j):
        a = s[:]
        a[i], a[j] = a[j], a[i]
        return a

    def solve(self):
        # 深度优先策略
        stack = [[self.start]]
        s = []  #解集
        while stack:
            c = stack.pop()
            if c[0] == self.end:
                s.append(reversed(c))
            else:
                for m in self.moves(c[0]):
                    stack.append([m] + c)
        return s

if __name__ == '__main__':
    halma = Halma(3)
    for s in halma.solve():
        for i in s:
            print i,
        print