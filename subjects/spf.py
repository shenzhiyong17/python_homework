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
        self.neibor = []

    def __str__(self):
        return "%s:%s map:%s" % (self.pos, self.blank, str(self.map))

    def __eq__(self, other):
        if other:
            return self.pos == other.pos
        return False

    def neighbor(self):
        if self.neibor:
            return self.neibor
        neighbor = []
        x, y = self.pos
        for h, r in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            pos = (h, r)
            if h in range(self.maze.long) and r in range(self.maze.width):
                if self.maze[pos].blank:
                    neighbor.append(self.maze[pos])
        self.neibor = neighbor
        return neighbor

    def set_map(self, dst, cost, nexthop):         # 更新map后要广播更新
        if not dst in self.map:
            self.map[dst] = {'cost': cost, 'nexthop': nexthop}
            self.broadcast(dst, cost)
        else:
            if cost < self.map[dst]['cost']:
                self.map[dst] = {'cost': cost, 'nexthop': nexthop}
                self.broadcast(dst, cost)

    def update(self, dst, cost, nexthop):          # 收到消息后更新自己的map
        if self.pos == self.maze.entrance or len(self.neighbor()) > 2:
            self.set_map(dst, cost + 1, nexthop.pos)
        else:
            self.broadcast(dst, cost + 1, exclude=nexthop)

    def broadcast(self, dst=None, cost=0, exclude=None):      # 广播自己的map中某一节点的信息
        if not dst:
            dst = self.pos
        for node in self.neighbor():
            if node == exclude:
                continue
            node.update(dst, cost, self)


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

    def path(self, src, dst):
        pre = p = self.maze[src]
        path = [p]
        while p != self.maze[dst]:
            if dst in p.map.keys():
                pre = p
                p = self.maze[p.map[dst]['nexthop']]
            else:
                for n in p.neighbor():
                    if n != pre:
                        pre = p
                        p = n
                        break
            path.append(p)
        return path

    def printpath(self, src, dst):
        if dst in self.maze[src].map:
            path = self.path(src, dst)
        else:
            raise RuntimeError('no way')
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
            # print entrance.map
            self.printpath(self.entrance, self.exit)
        else:
            raise RuntimeError('no way')

    def complete_convergence(self):         # 完全收敛,每个节点了解整张map
        for x in range(self.long):
            for y in range(self.width):
                node = self.maze[(x, y)]
                if node.blank:
                    node.broadcast()


if __name__ == '__main__':
    cnt = 0
    while True:
        cnt += 1
        print cnt
        try:
            m = Maze(25, 40, 60)
            t1 = timing(m.run)[0]
            print 't1: %s' % t1
            t2 = timing(m.complete_convergence)[0]
            print 't2: %s' %t2
            m.printpath(m.entrance, m.exit)
            break
        except RuntimeError:
            continue
