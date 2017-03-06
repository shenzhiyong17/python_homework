#!/usr/bin/env python
# date: 2016-2-2

import random, string


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


if __name__ == '__main__':
    print gen_rand_list(10)
    print gen_rand_string(50)
