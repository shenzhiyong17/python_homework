#!/usr/bin/python
# -*- coding:utf-8 -*-
# 在下面例子中，我们让boss与多个worker同时运行，并限制了queue不能放入多于3个元素。
# 这个限制意味着，直到queue有空余空间之前，put操作会被阻塞。相反地，如果队列中 没有元素，get操作会被阻塞。
# 它同时带一个timeout参数，允许在超时时间内如果 队列没有元素无法完成操作就抛出gevent.queue.Empty异常。


import gevent
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=3)


def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1)  # decrements queue size by 1
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')


def boss():
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """

    for i in xrange(1, 10):
        tasks.put(i)
    print('Assigned all work in iteration 1')

    for i in xrange(10, 20):
        tasks.put(i)
    print('Assigned all work in iteration 2')


gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'john'),
    gevent.spawn(worker, 'bob'),
])
