#!/usr/bin/python
# -*- coding:utf-8 -*-

# started -- 标志greenlet是否已经启动
# ready -- 标志greenlet是否已经被终止
# successful() -- 标志greenlet是否已经被终止，并且没有抛出异常
# value -- 由greenlet返回的值
# exception -- 在greenlet里面没有被捕获的异常

import gevent


def win():
    return 'You win!'


def fail():
    raise Exception('You fail at failing.')

winner = gevent.spawn(win)
loser = gevent.spawn(fail)

print(winner.started)   # True
print(loser.started)    # True

# Exceptions raised in the Greenlet, stay inside the Greenlet.
try:
    gevent.joinall([winner, loser])
except Exception as e:
    print('This will never be reached')

print(winner.value)     # 'You win!'
print(loser.value)      # None

print(winner.ready())   # True
print(loser.ready())    # True

print(winner.successful())  # True
print(loser.successful())   # False

# The exception raised in fail, will not propogate outside the
# greenlet. A stack trace will be printed to stdout but it
# will not unwind the stack of the parent.

print(loser.exception)

# It is possible though to raise the exception again outside
# raise loser.exception
# or with
# loser.get()