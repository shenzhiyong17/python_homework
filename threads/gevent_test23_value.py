#!/usr/bin/python
# -*- coding:utf-8 -*-

import gevent


def task(n):
    if n % 2 == 0:
        return n

numbers = [x for x in range(10)]
jobs = [gevent.spawn(task, n) for n in numbers]
gevent.joinall(jobs, timeout=5)

print [job.value for job in jobs]