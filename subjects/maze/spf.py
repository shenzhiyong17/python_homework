#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-05-11
# 简化spf算法做迷宫的解

from common.timing import timing
from subjects.maze.node import Node
from subjects.maze.absmaze import AbsMaze
import gevent
import time


class MyNode(Node):
    def __init__(self, x, y, blank, maze):
        Node.__init__(self, x, y, blank, maze)
        self.route_table = {self.pos: {'cost': 0, 'nexthop': self.pos}}

    def set_route(self, dst, cost, next_hop, bself, thread):  # 更新map后要广播更新
        if dst.pos not in self.route_table or self.route_table[dst.pos]['cost'] > cost:
            self.route_table[dst.pos] = {'cost': cost, 'nexthop': next_hop.pos}
            if thread:
                self.thread_broadcast(dst, cost, next_hop, bself)
            else:
                self.broadcast(dst, cost, next_hop, bself=bself)

    def update(self, dst, cost, next_hop, bself, thread=False):  # 收到消息后更新自己的map
        # print "%s %s %s %s" % (self.pos, dst.pos, next_hop.pos, cost)
        self.set_route(dst, cost + 1, next_hop, bself=bself, thread=thread)

    def broadcast(self, dst=None, cost=0, exclude=None, bself=False):  # 广播自己的map中某一节点的信息
        if not dst:
            dst = self
        for node in self.neighbor():
            if node == exclude:
                continue
            node.update(dst, cost, self, bself)
            if dst != self and bself:
                node.update(self, 0, self, bself)

    def thread_broadcast(self, dst=None, cost=0, exclude=None, bself=False):  # 广播自己的map中某一节点的信息
        if not dst:
            dst = self
        threads = []
        for node in self.neighbor():
            if node == exclude:
                continue
            threads.append(gevent.spawn(node.update, dst, cost, self, bself, True))
            if dst != self and bself:
                threads.append(gevent.spawn(node.update, self, cost, self, bself, True))
        gevent.joinall(threads)

    def gen_node(self, px, py, blank, maze):
        return MyNode(px, py, blank, maze)


class Map(AbsMaze):
    def __init__(self, x, y, per):  # 迷宫大小x * y. p为百分比.
        AbsMaze.__init__(self, x, y, per=per, node_class=MyNode)

    def reset(self):
        for node in self.map.itervalues():
            node.route_table = {node.pos: {'cost': 0, 'nexthop': node.pos}}

    def path(self, src, dst):  # 收敛后指出两点间路径
        if dst in self.map[src].route_table:
            p = self.map[src]
            path = [p]
            while p != self.map[dst]:
                p = self.map[p.route_table[dst]['nexthop']]
                path.append(p)
            return path
        else:
            raise RuntimeError('no way')

    def run(self, thread=False):
        exit = self.map[self.exit]
        entrance = self.map[self.entrance]
        if thread:
            exit.thread_broadcast()
        else:
            exit.broadcast()
        if self.exit in entrance.route_table:
            return
        else:
            raise RuntimeError('no way')

    def complete_convergence(self, thread=True):  # 完全收敛,每个节点了解整张map
        exit = self.map[self.exit]
        entrance = self.map[self.entrance]
        if thread:
            exit.thread_broadcast(bself=True)
        else:
            exit.broadcast(bself=True)
        if self.exit in entrance.route_table:
            return
        else:
            raise RuntimeError('no way')


def gen_and_solve_maze(save_path, x=15, y=40, percent_of_blank=60):
    cnt = 0
    while True:
        cnt += 1
        print cnt
        m = Map(x, y, percent_of_blank)
        try:
            t1 = timing(m.run)[0]
        except RuntimeError:
            continue
        m.print_path(m.path(m.entrance, m.exit))
        m.save_map(save_path)
        print 't1: %s, path length: %s' % (t1, len(m.path(m.entrance, m.exit)))
        break


def load_and_solve(path, process=True, thread=False, complete_convergence=False, thread_complete_convergence=False):
    m = Map(1, 1, 60)
    m.load_map(path)
    if process:
        t1 = timing(m.run)[0]
        path = m.path(m.entrance, m.exit)
        m.print_path(path)
        print 't1: %s, path length: %s' % (t1, len(path))
        time.sleep(2)
    if thread:
        m.reset()
        t2 = timing(m.run, True)[0]
        path = m.path(m.entrance, m.exit)
        m.print_path(m.path(m.entrance, m.exit))
        print 'thread broadcast spend: %s, path length: %s' % (t2, len(path))
    if complete_convergence:
        m.reset()
        t3 = timing(m.complete_convergence, False)[0]
        path = m.path(m.entrance, m.exit)
        m.print_path(m.path(m.entrance, m.exit))
        print 'complete convergence spend: %s, path length: %s' % (t3, len(path))
        print m.map[m.entrance].route_table
    if thread_complete_convergence:
        m.reset()
        t4 = timing(m.complete_convergence, True)[0]
        path = m.path(m.entrance, m.exit)
        m.print_path(m.path(m.entrance, m.exit))
        print 'threads complete convergence spend: %s, path length: %s' % (t4, len(path))
        print m.map[m.entrance].route_table


if __name__ == '__main__':
    # gen_and_solve_maze("maze.map", 10, 15, 60)
    load_and_solve("maze.map", process=False, thread=True, thread_complete_convergence=True, complete_convergence=True )
