#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17

import random
import time

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

    def printmaze(self):
        for x in range(self.long):
            for y in range(self.width):
                v, m = self.maze[(x, y)]
                if v == 0:
                    v = color_format(v, mode='highlight')
                print v,
            print '\n'

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

    def solvem(self):
        p = self.entrance
        while p != self.exit:
            x, y = p
            n = p
            for d in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
                if self.maze[d] == (0, False):
                    self.maze[d] = (0, True)
                    n = d
                    break
            if n != p:
                self.path.append(p)
                p = n
            elif not self.path:
                raise RuntimeError('no way')
            else:
                p = self.path.pop(-1)
            # print self.path
        self.path.append(p)
        return self.path


if __name__ == '__main__':
    while True:
        try:
            maze = Maze(25, 40, 60)
            # time.sleep(0.1)
            print maze.solvem()
            # maze.printmaze()
            print '========='
            maze.printpath()
            break
        except RuntimeError:
            print '==========='
            continue
