#!/usr/bin/python
# -*- coding:utf-8 -*-
# 在下面例子中，我们让boss与多个worker同时运行，并限制了queue不能放入多于3个元素。
# 这个限制意味着，直到queue有空余空间之前，put操作会被阻塞。相反地，如果队列中 没有元素，get操作会被阻塞。
# 它同时带一个timeout参数，允许在超时时间内如果 队列没有元素无法完成操作就抛出gevent.queue.Empty异常。

from gevent_test12_queue import job, Job
import gevent
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=3)


def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1)
            if isinstance(task, Job):
                task = task.do()
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')


def boss(job=None, n=20):
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """
    for i in xrange(1, n):
        something = job(i) if job else i
        tasks.put(something)
        print 'assigned job %s in queue' % i
    print('Assigned all work in iteration 1')


if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(boss, job, 8),
        gevent.spawn(boss, Job, 5),
        gevent.spawn(worker, 'steve'),
        gevent.spawn(worker, 'john'),
        gevent.spawn(worker, 'bob'),
    ])
