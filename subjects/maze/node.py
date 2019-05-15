#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2019.05.14

from abc import abstractmethod, ABCMeta
import json
import math


class Node:

    __metaclass__ = ABCMeta

    def __init__(self, px, py, blank, maze):
        self.maze = maze
        self.pos = (px, py)
        self.blank = blank  # 空或墙
        self.neigh = []

    @abstractmethod
    def gen_node(self, px, py, blank, maze):
        pass

    def __str__(self):
        node = {
            'pos': self.pos,
            'blank': self.blank
        }
        return json.dumps(node)

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
            if h in range(self.maze.long) and r in range(self.maze.width):
                if self.maze[pos].blank:
                    neighbor.append(self.maze[pos])
        self.neigh = neighbor
        return neighbor

    def distance(self, dst_pos):
        px, py = self.pos
        dis = int(math.fabs(px - dst_pos[0]) + math.fabs(py - dst_pos[1]))
        return dis
