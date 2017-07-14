#!/usr/bin/python
# -*- coding:utf-8 -*-
# 组(group)是一个运行中greenlet的集合，集合中的greenlet像一个组一样 会被共同管理和调度。
# 它也兼饰了像Python的multiprocessing库那样的 平行调度器的角色。
# 在管理异步任务的分组上它是非常有用的。就像上面所说，Group也以不同的方式为分组greenlet/分发工作和收集它们的结果也提供了API。

import gevent
from gevent import getcurrent
from gevent.pool import Group

group = Group()


def hello_from(n):
    print('Size of group %s' % len(group))
    print('Hello from Greenlet %s' % id(getcurrent()))


group.map(hello_from, xrange(3))


def intensive(n):
    gevent.sleep(3 - n)
    return 'task', n


print('Ordered')

ogroup = Group()
for i in ogroup.imap(intensive, xrange(3)):
    print(i)

print('Unordered')

igroup = Group()
for i in igroup.imap_unordered(intensive, xrange(3)):
    print(i)
