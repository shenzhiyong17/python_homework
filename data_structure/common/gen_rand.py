#!/usr/bin/env python
# date: 2016-2-2

import random
import string


def gen_rand_list(num, start=0, stop=1000):
    lst = []
    for i in range(num):
        x = random.randint(start, stop)
        lst.append(x)
    return lst


def gen_rand_string(length):
    s = string.letters + string.digits
    result = ''
    for i in xrange(length):
        result += s[random.randrange(len(s))]
    return result


def disorder(array):
    n = len(array)
    for i in range(n - 1):
        t = random.choice(range(i + 1, n))
        array[i], array[t] = array[t], array[i]
    return array
