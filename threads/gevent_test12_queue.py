#!/usr/bin/python
# -*- coding:utf-8 -*-
# 队列是一个排序的数据集合，它有常见的put / get操作， 但是它是以在Greenlet之间可以安全操作的方式来实现的。
# 举例来说，如果一个Greenlet从队列中取出一项，此项就不会被 同时执行的其它Greenlet再取到了。

import gevent
from gevent.queue import Queue

tasks = Queue()


def job(thing):
    msg = 'doing %s' % thing
    gevent.sleep(2)
    print 'doing job %s is done' % thing
    return msg


class Job:
    thing = None

    def __init__(self, thing):
        self.thing = thing

    def __str__(self):
        return self.thing

    def do(self):
        msg = 'do %s in class' % self.thing
        gevent.sleep(2)
        print 'Job %s is done' % self.thing
        return msg


def worker(name):
    while not tasks.empty():
        task = tasks.get()
        if isinstance(task, Job):
            task = task.do()
        print('Worker %s got task %s' % (name, task))
        gevent.sleep(0)

    print('Quitting time!')


def boss(job=None, n=25):
    # 如果job 是个function，put 的时候就已经运行了，只是放进去了结果，所以这儿最好放个对象，取出来的时候调接口运算结果
    for i in xrange(1, n):
        tasks.put_nowait(job(i))  # put_nowait和get_nowait不会阻塞


if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(boss, job, 8),
        gevent.spawn(boss, Job),
    ])
    gevent.joinall([
        gevent.spawn(worker, 'a'),
        gevent.spawn(worker, 'b'),
        gevent.spawn(worker, 'c'),
    ])
