#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-04-17
# 迷宫的解

from common.timing import timing
import gevent
from subjects.maze.node import Node
from subjects.maze.absmaze import AbsMaze


class MyNode(Node):
    def __init__(self, px, py, blank, maze):
        Node.__init__(self, px, py, blank, maze)
        self.bread = False

    def gen_node(self, px, py, blank, maze):
        return MyNode(px, py, blank, maze)


class Maze(AbsMaze):
    def __init__(self, sx, sy, per=75):  # 迷宫大小x * y. p为空格百分比.
        AbsMaze.__init__(self, sx, sy, per=per, node_class=MyNode)
        self.done = False

    def reset(self):
        for node in self.map.itervalues():
            node.bread = False

    def solve(self):
        # 找出一条路径到达出口,然后简化掉其中环路
        p = self.map[self.entrance]
        path = []
        while p.pos != self.exit:
            n = p
            for nei in p.neighbor():
                if nei.blank:
                    if not nei.bread:
                        nei.bread = True
                        n = nei
                        break
            if n != p:  # 前进了一格
                path.append(p)
                p = n
            elif not path:  # 没有路
                raise RuntimeError('no way')
            else:  # 后退一格
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

    def solve_threads(self):
        def walk(path):
            if not self.done:
                threads = []
                for nei in path[-1].neighbor():
                    if nei.pos == self.exit:
                        path.append(nei)
                        self.done = True
                        return path
                    if nei.blank and not nei.bread:
                        nei.bread = True
                        threads.append(gevent.spawn(walk, path + [nei]))
                gevent.joinall(threads)
                for thread in threads:
                    if thread.value:
                        return thread.value

        p = self.map[self.entrance]
        p.bread = True
        path = [p]
        res = walk(path)
        if res:
            return res
        else:
            raise RuntimeError('no way')

    def solve_all(self, first=False):
        # 深度优先策略,找出所有解, first=True 时找到地一个解就退出
        # 性能差，不可用。
        stack = [[self.map[self.entrance]]]
        s = []
        while stack:
            path = stack.pop()
            if path[-1].pos == self.exit:
                s.append(path)
                if first:
                    return s
            else:
                for nei in path[-1].neighbor():
                    if nei not in path and nei.blank is True:
                        stack.append(path + [nei])
        if s:
            return s
        else:
            raise RuntimeError('no way')


def gen_maze_and_resolve(x=20, y=40, percent_of_blank=60, solve_thread=True, solve_all=False, solve_all_first=True):
    count = 1
    while True:
        try:
            print count
            maze = Maze(x, y, percent_of_blank)
            t1, path = timing(maze.solve)
            print 'count: %s' % count
            maze.print_path(path)
            maze.reset()
            print "t1: %s" % t1

            if solve_thread:
                t2, path = timing(maze.solve_threads)
                maze.print_path(path)
                maze.reset()
                print "t2: %s" % t2

            if solve_all:
                t3, s = timing(maze.solve_all, solve_all_first)
                maze.print_path(s[0])
                maze.reset()
                print "t3: %s" % t3

            break
        except RuntimeError:
            count += 1
            continue


def load_map_and_resolve(path="maze.map", solve=True, solve_thread=True):
    maze = Maze(1, 1, 60)
    maze.load_map(path)

    if solve:
        t1, path = timing(maze.solve)
        maze.print_path(path)
        maze.reset()
        print "basic solve: %s, path length: %s" % (t1, len(path))

    if solve_thread:
        t2, path = timing(maze.solve_threads)
        maze.print_path(path)
        maze.reset()
        print "threads solve: %s, path length: %s" % (t2, len(path))


if __name__ == '__main__':
    # gen_maze_and_resolve()
    load_map_and_resolve(solve=True, solve_thread=True)


