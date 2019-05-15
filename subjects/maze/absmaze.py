#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2019.05.14

from abc import abstractmethod, ABCMeta
from tools.colorFormat import color_format
from itertools import islice
import random
import json
import os


class AbsMaze:
    __metaclass__ = ABCMeta

    def __init__(self, sx, sy, node_class, per=75):  # 迷宫大小x * y. p为空格百分比.
        self.map = {}
        self.node = node_class
        for x in range(sx):
            for y in range(sy):
                if random.randint(0, 100) < per:
                    self.map[(x, y)] = self.node(x, y, True, self)
                else:
                    self.map[(x, y)] = self.node(x, y, False, self)
        self.entrance = (0, 0)
        self.exit = (sx - 1, sy - 1)
        self.map[self.entrance].blank = True
        self.map[self.exit].blank = True
        self.long = sx
        self.width = sy

    def __getitem__(self, pos):
        return self.map[pos]

    def save_map(self, map_file):
        if os.path.exists(map_file):
            os.remove(map_file)
        with open(map_file, 'w') as f:
            for pos in self.map.iterkeys():
                f.write("%s\n" % self.map[pos])

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
                self.map[(x, y)] = self.node(x, y, blank, self)
                if x > long:
                    long = x
                if y > width:
                    width = y
            except Exception as e:
                print pos_line
                raise e
        map.close()
        self.long = long + 1
        self.width = width + 1
        self.exit = (long, width)
        self.map[self.entrance].blank = True
        self.map[self.exit].blank = True

    @abstractmethod
    def reset(self):
        pass

    def print_path(self, path):
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
