#!/usr/bin/env python

def conflict(state, nextX):
    nextY = len(state)
    for i in range(nextY):
        if abs(state[i] - nextX) in (0, nextY - i):
            return True
    return False


def queens(num=8, state=()):
    for pos in range(num):
        if not conflict(state, pos):
            if len(state) == num - 1:
                print state
                yield (pos,)
            else:
                for result in queens(num, state + (pos,)):
                    print "=========", result
                    yield result + (pos,)


def prettyprint(solution):
    def line(pos, length=len(solution)):
        return ". " * pos + "X " + ". " * (length - pos - 1)

    for pos in solution:
        print line(pos)


import random

prettyprint(random.choice(list(queens(6))))

# q = queens(8)
# print q.next()
# for i in q :
#     print i
