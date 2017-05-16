#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-05-11
# 简化spf算法做迷宫的解

import random

from tools.colorFormat import color_format
from common.timing import timing


class Node:
    def __init__(self, x, y, blank, maze):
        self.maze = maze
        self.pos = (x, y)
        self.blank = blank
        self.map = {self.pos: {'cost': 0, 'nexthop': self.pos}}

    def __str__(self):
        return "%s:%s map:%s" % (self.pos, self.blank, str(self.map))

    def neighbor(self):
        neighbor = []
        x, y = self.pos
        for h, r in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            pos = (h, r)
            if h in range(self.maze.long) and r in range(self.maze.width):
                if self.maze[pos].blank:
                    neighbor.append(self.maze[pos])
        return neighbor

    def set_map(self, pos, cost, nexthop):         # 更新map后要广播更新
        if not pos in self.map:
            self.map[pos] = {'cost': cost, 'nexthop': nexthop}
            self.broadcast(pos, cost)
        else:
            if cost < self.map[pos]['cost']:
                self.map[pos] = {'cost': cost, 'nexthop': nexthop}
                self.broadcast(pos, cost)

    def update(self, pos, cost, node):          # 收到消息后更新自己的map
        self.set_map(pos, cost + 1, node.pos)

    def broadcast(self, pos=None, cost=0):      # 广播自己的map中某一节点的信息
        if not pos:
            pos = self.pos
        for node in self.neighbor():
            node.update(pos, cost, self)


class Maze:
    def __init__(self, long, width, per=75):    # 迷宫大小x * y. p为百分比.
        self.long = long
        self.width = width
        self.maze = {}
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
            p = self.maze[p.map[self.exit]['nexthop']]
            path.append(p)
        return path

    def printpath(self, path):
        head = '  '
        for y in range(self.width):
            head += ' %2s' % y
        print head
        for x in range(self.long):
            print '%2s' %x,
            for y in range(self.width):
                try:
                    v = self.maze[(x, y)]
                    if v in path:
                        v = color_format(' X', mode='highlight')
                    elif v.blank:
                        v = '  '
                    else:
                        v = ' ='
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
            print entrance.map
            path = self.path()
            self.printpath(path)
        else:
            raise RuntimeError('no way')

    def complete_convergence(self):         # 完全收敛,每个节点了解整张map
        entrance = self.maze[self.entrance]
        for x in range(self.long):
            for y in range(self.width):
                node = self.maze[(x, y)]
                if node.blank:
                    node.broadcast()
        if self.exit in entrance.map:
            print '%s\'s map (%s): ' % (entrance.pos, len(entrance.map))
            for pos in entrance.map.keys():
                print '\t%s: %s' %(pos, entrance.map[pos])
            path = self.path()
            self.printpath(path)
        else:
            raise RuntimeError('no way')


if __name__ == '__main__':
    cnt = 0
    while True:
        cnt += 1
        print 'cnt: %s' %cnt
        try:
            m = Maze(25, 40, 65)
            t1 = timing(m.run)[0]
            print 't1: %s' % t1
            t2 = timing(m.complete_convergence)[0]
            print 't2: %s' %t2
            break
        except RuntimeError:
            continue
