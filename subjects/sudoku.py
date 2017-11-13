#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-11-10

import random


class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.valid = [i for i in range(1, 10)]

    def init(self):
        self.value = None
        self.valid = [i for i in range(1, 10)]

    def __str__(self):
        return "x:%s, y:%s, value:%s" % (self.x, self.y, self.value)

    def set_value(self, value):
        self.value = value
        return self


class SudoKu:
    def __init__(self):
        self.matrix = []
        for y in range(9):
            for x in range(9):
                self.matrix.append(cell(x, y))

    def sub_matrix(self, sub_index):
        # 小九格，sub_index: 0~8
        indexs = []
        res = []
        for i in range(3):
            for j in range(3):
                indexs.append((sub_index / 3 * 3 + i) * 9 + sub_index % 3 * 3 + j)
        for index in indexs:
            res.append(self.matrix[index])
        return res

    def get_cells(self, h=None, v=None, cell=None):
        # p: 同一行， v: 同一列， p: 同一格
        if h is not None:
            return self.matrix[h * 9: h * 9 + 9]
        if v is not None:
            return self.matrix[v::9]
        if cell is not None:
            n = cell.x + cell.y * 9  # index of matrix
            sub_index = (n / 27) * 3 + (n % 9 / 3)
            return self.sub_matrix(sub_index)

    def conflict(self, cell):
        # 冲突True， 不冲突False
        value = cell.value
        for i in self.get_cells(h=cell.y):
            if cell.x != i.x and value == i.value:
                return True
        for i in self.get_cells(v=cell.x):
            if cell.y != i.y and value == i.value:
                return True
        for i in self.get_cells(cell=cell):
            if i.x != cell.x and i.y != cell.y and i.value == value:
                return True
        return False

    def fill_random(self, cell):
        tmp = list(cell.valid)
        random.shuffle(tmp)
        for value in tmp:
            if not self.conflict(cell.set_value(value)):
                return True
            else:
                cell.valid.remove(value)
        return False

    def init_matrix(self, pos=0):
        deep = 1
        while pos < 81:
            for cell in self.matrix[pos + 1:deep]:
                cell.init()
            # print 'pos: %s' % pos
            cell = self.matrix[pos]
            if cell.value is not None:
                cell.valid.remove(cell.value)
                cell.value = None
            if not cell.valid or not self.fill_random(cell):
                pos -= 1
            else:
                pos += 1
            if not deep > pos:
                deep = pos + 1

    def pr_pazzle(self, percent=100):
        i = 0
        for cell in self.matrix:
            if i % 27 == 0:
                print '---------------------------'
            if i % 3 == 0:
                print "|",
            if random.randint(1, 100) <= percent:
                print cell.value,
            else:
                print ' ',
            i += 1
            if i % 9 == 0:
                print '|'
        print '---------------------------'


if __name__ == '__main__':
    sudoku = SudoKu()
    sudoku.init_matrix()
    sudoku.pr_pazzle(40)
    print '\n' * 10
    sudoku.pr_pazzle(100)
