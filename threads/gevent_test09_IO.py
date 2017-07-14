#!/usr/bin/python
# -*- coding:utf-8 -*-
# 同时对同一个文件进行写操作，结果很赞

import gevent
import time

out_file = '/tmp/gevent_test.log'
start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)


def write(out_file, message):
    f = open(out_file, 'a')
    f.write('%s %s \n' % (message, tic()))
    gevent.sleep(1)
    f.write('%s again %s \n' %(message, tic()))
    f.close()



def read(read_file):
    f = open(read_file, 'r')
    print f.read()
    f.close()

threads = []
for id in range(1, 10):
    threads.append(gevent.spawn(write, out_file, str(id)))
gevent.joinall(threads)


