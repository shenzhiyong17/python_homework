#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-05-11
# 简化spf算法做迷宫的解

import random

from tools.colorFormat import color_format
from common.timing import timing
from itertools import islice
import json
import os


class Node:
    def __init__(self, x, y, blank, map):
        self.map = map
        self.pos = (x, y)
        self.blank = blank
        self.route_table = {self.pos: {'cost': 0, 'nexthop': self.pos}}
        self.neigh = []

    def __str__(self):
        pos = {
            'pos': self.pos,
            'blank': self.blank
            # 'route_table': self.route_table
        }
        return json.dumps(pos)

    def __eq__(self, other):
        if other:
            return self.pos == other.pos
        return False

    def neighbor(self):
        if self.neigh:
            return self.neigh
        neighbor = []
        x, y = self.pos
        for h, r in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            pos = (h, r)
            if h in range(self.map.long) and r in range(self.map.width):
                if self.map[pos].blank:
                    neighbor.append(self.map[pos])
        self.neigh = neighbor
        return neighbor

    def set_route(self, dst, cost, nexthop):  # 更新map后要广播更新
        if dst not in self.route_table or self.route_table[dst]['cost'] > cost:
            self.route_table[dst] = {'cost': cost, 'nexthop': nexthop}
            self.broadcast(dst, cost)

    def update(self, dst, cost, nexthop):  # 收到消息后更新自己的map
        self.set_route(dst, cost + 1, nexthop.pos)

    def broadcast(self, dst=None, cost=0, exclude=None):  # 广播自己的map中某一节点的信息
        if not dst:
            dst = self.pos
        for node in self.neighbor():
            if node == exclude:
                continue
            node.update(dst, cost, self)


class Map:
    def __init__(self, long=1, width=1, per=75):  # 迷宫大小x * y. p为百分比.
        self.long = long
        self.width = width
        self.map = {}
        for x in range(long):
            for y in range(width):
                if random.randint(0, 100) < per:
                    self.map[(x, y)] = Node(x, y, True, self)  # 指定几率改为通路
                else:
                    self.map[(x, y)] = Node(x, y, False, self)
        self.entrance = (0, 0)
        self.exit = (long - 1, width - 1)
        self.map[self.entrance].blank = True
        self.map[self.exit].blank = True

    def __getitem__(self, pos):
        return self.map[pos]

    def path(self, src, dst):  # 收敛后指出两点间路径
        p = self.map[src]
        path = [p]
        while p != self.map[dst]:
            p = self.map[p.route_table[dst]['nexthop']]
            path.append(p)
        return path

    def printpath(self, src, dst):
        if dst in self.map[src].route_table:
            path = self.path(src, dst)
        else:
            raise RuntimeError('no way')
        head = '  '
        for y in range(self.width):
            head += ' %2s' % y
        print head
        for x in range(self.long):
            print '%2s' % x,
            for y in range(self.width):
                try:
                    v = self.map[(x, y)]
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

    def save_map(self, map_file):
        save = open(map_file, 'w')
        for pos in self.map:
            save.write("%s\n" % self.map[pos])
        save.close()

    def load_map(self, map_file):
        if not os.path.exists(map_file):
            raise IOError("%s not exist" % map_file)
        map = open(map_file, 'r')
        long = 1
        width = 1
        self.map = {}
        for pos_line in islice(map, 0, None):
            try:
                js = json.loads(pos_line)
                x, y = js['pos']
                x = int(x)
                y = int(y)
                blank = js['blank']
                self.map[(x, y)] = Node(x, y, blank, self)
                if x > long:
                    long = x
                if y > width:
                    width = y
            except Exception as e:
                print pos_line
                raise e
        map.close()
        self.long = long
        self.width = width
        self.exit = (long - 1, width - 1)
        self.map[self.entrance].blank = True
        self.map[self.exit].blank = True

    def run(self):
        exit = self.map[self.exit]
        entrance = self.map[self.entrance]
        exit.broadcast()
        if self.exit in entrance.route_table:
            return
        else:
            raise RuntimeError('no way')

    def complete_convergence(self):  # 完全收敛,每个节点了解整张map
        for x in range(self.long):
            for y in range(self.width):
                node = self.map[(x, y)]
                if node.blank:
                    node.broadcast()


if __name__ == '__main__':
    cnt = 0
    while True:
        cnt += 1
        print cnt
        try:
            m = Map(15, 40, 60)
            t1 = timing(m.run)[0]
            if len(m.path(m.entrance, m.exit)) < (15 + 40) * 1.6:
                if cnt > 10000:
                    break
                continue
            m.printpath(m.entrance, m.exit)
            m.save_map('/tmp/maze.map')
            print 't1: %s' % t1
            t2 = timing(m.complete_convergence)[0]
            print 't2: %s' % t2
            m.printpath(m.entrance, m.exit)
            m.load_map('/tmp/maze.map')
            t1 = timing(m.run)[0]
            m.printpath(m.entrance, m.exit)
            break
        except RuntimeError:
            continue
