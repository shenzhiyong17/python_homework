#!/usr/bin/python
# -*- coding:utf-8 -*-
# 同时对同一个文件进行写操作，结果很赞

import gevent
import time

out_file = '/tmp/gevent_test.log'
start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)


def output(out_file, message):
    f = open(out_file, 'a')
    f.write('%s %s \n' % (message, tic()))
    gevent.sleep(1)
    f.write('%s again %s \n' %(message, tic()))
    f.close()


threads = []
for i in range(1, 10):
    threads.append(gevent.spawn(output, out_file, str(i)))
for i in range(1, 10):
    threads.append(gevent.spawn(output, out_file, str(i*20)))
gevent.joinall(threads)


