#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-05-03
# 8皇后 深度优先


class Queen():
    def __init__(self, size=8):
        self.size = size

    @staticmethod
    def valid(state, pos):
        for index in range(len(state)):
            p = state[index]
            if pos == p:
                return False
            if abs(p - pos) == len(state) - index:
                return False
        return True

    def mirror(self, state):
        res = []
        for pos in state:
            res.append(self.size - 1 - pos)
        return res

    def solve_all(self):
        s = []
        stack = []
        for pos in range(self.size / 2 + 1):
            stack.append([pos])
        while stack:
            state = stack.pop(-1)  # 从最后拿出,再放到最后去,深度优先
            if len(state) == self.size:
                s.append(state)
                # break                       # 只求一个结果
            else:
                for pos in range(self.size):
                    if self.valid(state, pos):
                        stack.append(state + [pos])
        for state in s:
            if state[0] < (self.size / 2):
                s.append(self.mirror(state))
        return s

    @staticmethod
    def print_s(state):
        for pos in state:
            print ". " * pos + "X " + ". " * (len(state) - pos - 1)

    def run(self):
        for state in self.solve_all():
            self.print_s(state)
            print '==============\n'


if __name__ == '__main__':
    q = Queen(5)
    print len(q.solve_all())
    q.run()
