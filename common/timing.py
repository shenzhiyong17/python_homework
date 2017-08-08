#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

start = time.time()
tic = lambda: '%.1f' % (time.time() - start)


def timing(function, *args):
    t1 = time.time()
    res = function(*args)
    t2 = time.time()
    return (t2 - t1, res)
