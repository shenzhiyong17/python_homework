#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17
# 迷宫的解

import random

from tools.colorFormat import color_format


class Maze():
    def __init__(self, long, width, per=75):  # 迷宫大小x * y. p为百分比.
        # {(x,y)=(v,m)..}    x,y-坐标,v-0为通道1为墙,m-面包屑
        self.maze = {}
        for x in range(long):
            for y in range(width):
                self.maze[(x, y)] = ('=', False)
        for x in range(1, long - 1):
            for y in range(1, width - 1):
                if random.randint(0, 100) < per:
                    self.maze[(x, y)] = (0, False)
        self.entrance = (1, 1)
        self.exit = (long - 2, width - 2)
        self.maze[self.entrance] = (0, False)
        self.maze[self.exit] = (0, False)
        self.long = long
        self.width = width

    def printpath(self, path):
        for x in range(self.long):
            for y in range(self.width):
                v, m = self.maze[(x, y)]
                if (x, y) in path:
                    v = color_format('X', mode='highlight')
                elif v == 0:
                    v = ' '
                print v,
            print ''
        print '***************************'

    def around(self, p):
        x, y = p
        return (x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)

    def solve(self):
        # 找出一条路径到达出口,然后简化掉其中环路
        p = self.entrance
        path = []
        while p != self.exit:
            n = p
            for d in self.around(p):
                if self.maze[d] == (0, False):
                    self.maze[d] = (0, True)
                    n = d
                    break
            if n != p:
                path.append(p)
                # for around in self.around(n):       # 优化path,去掉环路
                #     try:
                #         if around != p and self.maze[around] == (0, True):
                #             while True:
                #                 if path.pop(-1) == around:
                #                     break
                #             path.append(around)
                #     except KeyError:
                #         continue
                #     except IndexError:
                #         raise RuntimeError('no way')
                p = n
            elif not path:
                raise RuntimeError('no way')
            else:
                p = path.pop(-1)
        path.append(p)
        print '================'

        index = 0
        while index < len(path) - 2:  # 优化path,去掉环路
            p = path[index]
            for around in self.around(p):
                if around in path[index + 2:]:
                    while True:
                        if path.pop(index + 1) == around:
                            break
                    path.insert(index + 1, around)
            index += 1
        return path

    def solve1(self):
        # 找出相对短的路由
        # 如果下一步离目的更近则继续,否则切换到另一条路
        pass

    def solve_all(self):
        # 深度优先策略,找出所有解
        stack = [[self.entrance]]
        s = []
        while stack:
            path = stack.pop()
            if path == self.exit:
                s.append(path)
            else:
                for p in self.around(path[-1]):
                    if not p in path and self.maze[p][0] == 0:
                        stack.append(path + [p])
        return s

if __name__ == '__main__':
    count = 1
    x = 25
    y = 80
    while True:
        try:
            maze = Maze(x, y, 60)
            path = maze.solve()
            print 'count: %s' % count
            maze.printpath(path)
            break
        except RuntimeError:
            count += 1
            continue
