#!/usr/bin/env python

from math import sqrt


def exercise1_3(num, stat=()):
    if len(stat) == num:
        yield stat
    else:
        for r in True, False:
            for result in exercise1_3(num, stat+(r,)):
                yield result

def exercise1_6(num):
    sq = sqrt(num)
    lst = list([x for x in range(2,int(sq))])
    result = []
    while lst:
        i = lst[0]
        if num % i == 0:
            result.append(i)
            result.append(num/i)
        lst.remove(i)
    if sq % 1 == 0 : result.append(int(sq))
    return result


def exercise1_7_r(num):
    if num <= 1:
        return 1
    else:
        return num*exercise1_7_r(num-1)

def exercise1_7_l(num):
    result = 1
    if not num <= 1:
        for i in range(1,num+1):
            result *= i
    return result

def fib_r(num):
    # exercise1_8
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fib_r(num -2) + fib_r(num - 1)

def fib_l(num):
    result = (0,1)
    if num == 0 or num == 1:
        return result[num]
    else:
        for i in range(2,num+1):
            result = (result[1], result[0] + result[1])
        return result[1]

def ackerman_r(m, n):
    # exercise1_10
    if m == 0:
        return n+1
    elif n == 0:
        return ackerman_r(m-1, 1)
    else:
        return ackerman_r(m-1, ackerman_r(m, n-1))

def ackerman_l(m, n):
    result = [m, n]
    while not len(result) == 1:
        if result[-2] == 0:
            result[-2:] = [result[-1]+1 ]
        elif result[-1] == 0:
            result[-2:] = [result[-2]-1, 1]
        else:
            result[-2:] = [result[-2]-1, result[-2], result[-1]-1]
    return result[0]

def hanoi(num, a, b, c):
    # exercise1_11
    if num == 1:
        print '%-3s,%s -> %s' %(num*'-', a, c)
    else:
        hanoi(num-1, a,c,b)
        print '%-3s,%s -> %s' %(num*'-', a, c)
        hanoi(num-1,b,a,c)

def powerset(s, a=None):
    # exercise1_12
    if not a:
        a = s[0]
        s = s[1:]
    if not s:
        return (),(a,)
    else:
        r = ()
        for x in powerset(s[1:], s[0]):
            r = r + ( (x  + (a,) ),)
        return powerset(s[1:], s[0]) + r

if __name__ == '__main__':
    # s = tuple(gen_rand.gen_rand_list(4))
    s = ('a','b','c')
    print s
    print powerset(s)
