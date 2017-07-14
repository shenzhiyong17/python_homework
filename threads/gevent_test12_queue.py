#!/usr/bin/python
# -*- coding:utf-8 -*-
# 队列是一个排序的数据集合，它有常见的put / get操作， 但是它是以在Greenlet之间可以安全操作的方式来实现的。
# 举例来说，如果一个Greenlet从队列中取出一项，此项就不会被 同时执行的其它Greenlet再取到了。

import gevent
from gevent.queue import Queue

tasks = Queue()


def worker(n):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (n, task))
        gevent.sleep(0)

    print('Quitting time!')


def boss():
    for i in xrange(1, 25):
        tasks.put_nowait(i)  # put_nowait和get_nowait不会阻塞


gevent.spawn(boss).join()
gevent.joinall([
    gevent.spawn(worker, 'a'),
    gevent.spawn(worker, 'b'),
    gevent.spawn(worker, 'c'),
])
