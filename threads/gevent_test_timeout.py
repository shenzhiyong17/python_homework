#!/usr/bin/python
# -*- coding:utf-8 -*-

import gevent
from gevent import Timeout


def wait():
    gevent.sleep(3)

seconds = 2

timeout = Timeout(seconds)
timeout.start()

try:
    gevent.spawn(wait).join()
except Timeout:
    print 'Could not complete'

# --

timer = Timeout(1).start()
thread1 = gevent.spawn(wait)

try:
    thread1.join(timeout=timer)
except Timeout:
    print('Thread 1 timed out')

# --

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait)

try:
    thread2.get(timeout=timer)
except Timeout:
    print('Thread 2 timed out')

# --

try:
    gevent.with_timeout(1, wait)
except Timeout:
    print('Thread 3 timed out')
