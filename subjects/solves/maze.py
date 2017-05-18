#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17
# 迷宫的解

import random

from tools.colorFormat import color_format
from common.timing import timing


class Maze:
    class Node:
        def __init__(self, px, py, blank, maze):
            self.maze = maze
            self.pos = (px, py)
            self.blank = blank
            self.bread = False
            self.neigh = None

        def __str__(self):
            return str(self.pos)

        def __eq__(self, other):
            if other:
                return self.pos == other.pos
            return False

        def neighbor(self):
            if self.neigh is not None:
                return self.neigh
            neighbor = []
            px, py = self.pos
            for h, r in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                pos = (h, r)
                if h in range(self.maze.long) and r in range(self.maze.width):
                    if self.maze[pos].blank:
                        neighbor.append(self.maze[pos])
            self.neigh = neighbor
            return neighbor

    def __init__(self, sx, sy, per=75):  # 迷宫大小x * y. p为百分比.
        # {(x,y)=(v,m)..}    x,y-坐标,v-0为通道1为墙,m-面包屑
        self.map = {}
        for x in range(sx):
            for y in range(sy):
                if random.randint(0, 100) < per:
                    self.map[(x, y)] = self.Node(x, y, True, self)
                else:
                    self.map[(x, y)] = self.Node(x, y, False, self)
        self.entrance = (0, 0)
        self.exit = (sx - 1, sy - 1)
        self.map[self.entrance].blank = True
        self.map[self.exit].blank = True
        self.long = sx
        self.width = sy

    def __getitem__(self, pos):
        return self.map[pos]

    def printpath(self, path):
        head = '  '
        for y in range(self.width):
            head += ' %2s' % y
        print head
        for x in range(self.long):
            print '%2s' % x,
            for y in range(self.width):
                v = self.map[(x, y)]
                if v in path:
                    print color_format(' X', mode='highlight'),
                elif v.blank:
                    print '  ',
                else:
                    print ' =',
            print ''
        print '***************************'

    def solve(self):
        # 找出一条路径到达出口,然后简化掉其中环路
        p = self.map[self.entrance]
        path = []
        while p.pos != self.exit:
            n = p
            for d in p.neighbor():
                if d.blank:
                    if not d.bread:
                        d.bread = True
                        n = d
                        break
            if n != p:
                # print n,p
                path.append(p)
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
            for nei in p.neighbor():
                if nei in path[index + 2:]:
                    while True:
                        if path.pop(index + 1) == nei:
                            break
                    path.insert(index + 1, nei)
            index += 1
        return path

    def solve_all(self):
        # 深度优先策略,找出所有解
        stack = [[self.map[self.entrance]]]
        s = []
        while stack:
            path = stack.pop()
            if path == self.exit:
                s.append(path)
            else:
                for p in path[-1].neighbor():
                    if not p in path and self.map[p][0] == 0:
                        stack.append(path + [p])
        return s


if __name__ == '__main__':
    count = 1
    x = 25
    y = 80
    while True:
        try:
            print count
            maze = Maze(x, y, 60)
            t, path = timing(maze.solve)
            print 'count: %s' % count
            maze.printpath(path)
            print t
            break
        except RuntimeError:
            count += 1
            continue
