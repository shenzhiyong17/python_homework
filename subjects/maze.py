#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17

import random

from tools.colorFormat import color_format


class Maze():
    def __init__(self, long, width, per=75):  # 迷宫大小x * y. p为百分比.
        # {(x,y)=(v,m)..}    x,y-坐标,v-0为通道1为墙,m-面包屑
        self.maze = {}
        for x in range(long):
            for y in range(width):
                self.maze[(x, y)] = ('.', False)
        for x in range(1, long - 1):
            for y in range(1, width - 1):
                if random.randint(0, 100) < per:
                    self.maze[(x, y)] = (0, False)
        self.entrance = (1, 1)
        self.exit = (long - 2, width - 2)
        self.maze[self.entrance] = (0, False)
        self.maze[self.exit] = (0, False)
        self.path = []
        self.long = long
        self.width = width

    def printpath(self):
        for x in range(self.long):
            for y in range(self.width):
                v, m = self.maze[(x, y)]
                if (x, y) in self.path:
                    v = color_format('X', mode='highlight')
                elif v == 0:
                    v = ' '
                print v,
            print '\n'

    def around(self, p):
        x, y = p
        return (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)

    def solvem(self):
        p = self.entrance
        while p != self.exit:
            n = p
            for d in self.around(p):
                if self.maze[d] == (0, False):
                    self.maze[d] = (0, True)
                    n = d
                    break
            if n != p:
                self.path.append(p)
                # for around in self.around(n):       # 优化path,去掉环路
                #     try:
                #         if around != p and self.maze[around] == (0, True):
                #             while True:
                #                 if self.path.pop(-1) == around:
                #                     break
                #             self.path.append(around)
                #     except KeyError:
                #         continue
                #     except IndexError:
                #         raise RuntimeError('no way')
                p = n
            elif not self.path:
                raise RuntimeError('no way')
            else:
                p = self.path.pop(-1)
        self.path.append(p)
        print '================'

        index = 0
        while index < len(self.path) - 2:        # 优化path,去掉环路
            p = self.path[index]
            for around in self.around(p):
                if around in self.path[index+2:]:
                    while True:
                        if self.path.pop(index+1) == around:
                            break
                    self.path.insert(index + 1, around)
            index += 1
        return self.path

if __name__ == '__main__':
    count = 1
    while True:
        try:
            maze = Maze(25, 50, 65)
            maze.solvem()
            print 'count: %s' %count
            print '========='
            maze.printpath()
            break
        except RuntimeError:
            # print '==========='
            count += 1
            continue

