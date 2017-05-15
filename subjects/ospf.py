#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-05-11
# ospf算法做迷宫的解

import random

from tools.colorFormat import color_format


class Node:
    def __init__(self, x, y, blank, maze):
        self.maze = maze
        self.pos = (x, y)
        self.blank = blank
        self.map = {}

    def __str__(self):
        return "%s:%s" % (self.pos, self.blank)

    def neighbor(self):
        neighbor = []
        x, y = self.pos
        for h, r in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            pos = (h, r)
            if h in range(self.maze.long) and r in range(self.maze.width):
                if self.maze[pos].blank:
                    neighbor.append(self.maze[pos])
        return neighbor

    def set_map(self, pos, cost, node):
        if not pos in self.map:
            self.map[pos] = {'cost': cost, 'from': node.pos}
            self.broadcast(pos, cost)
        else:
            if cost < self.map[pos]['cost']:
                self.map[pos] = {'cost': cost, 'from': node.pos}
                self.broadcast(pos, cost)

    def hello(self, node, map):
        for pos in map.keys():
            node.set_map(pos, map[pos]['cost'], map['from'])

    def update(self, pos, cost, node):
        self.set_map(pos, cost + 1, node)

    def broadcast(self, pos=None, cost=0):
        if not pos:
            pos = self.pos
        for node in self.neighbor():
            # print node
            node.update(pos, cost, self)


class Maze:
    def __init__(self, long, width, per=75):  # 迷宫大小x * y. p为百分比.
        self.long = long
        self.width = width
        self.maze = {}
        for x in range(long):
            for y in range(width):
                self.maze[(x, y)] = None  # 默认是墙
        for x in range(long):
            for y in range(width):
                if random.randint(0, 100) < per:
                    self.maze[(x, y)] = Node(x, y, True, self)  # 指定几率改为通路
                else:
                    self.maze[(x, y)] = Node(x, y, False, self)
        self.entrance = (0, 0)
        self.exit = (long - 1, width - 1)
        self.maze[self.entrance].blank = True
        self.maze[self.exit].blank = True

    def __getitem__(self, pos):
        return self.maze[pos]

    def path(self):
        p = self.maze[self.entrance]
        path = [p]
        while p != self.maze[self.exit]:
            # print p
            p = self.maze[p.map[self.exit]['from']]
            path.append(p)
        return path

    def printpath(self, path):
        for x in range(self.long):
            for y in range(self.width):
                try:
                    v = self.maze[(x, y)]
                    if v in path:
                        v = color_format('X', mode='highlight')
                    elif v.blank:
                        v = ' '
                    else:
                        v = '='
                    print v,
                except AttributeError as e:
                    print x, y, e
                    raise
            print ''
        print '***************************'

    def run(self):
        exit = self.maze[self.exit]
        entrance = self.maze[self.entrance]
        exit.broadcast()
        if self.exit in entrance.map:
            path = self.path()
            self.printpath(path)
        else:
            raise RuntimeError('no way')


if __name__ == '__main__':
    cnt = 0
    while True:
        cnt += 1
        try:
            m = Maze(25, 80, 60)
            m.run()
            break
        except RuntimeError:
            continue
    print cnt
