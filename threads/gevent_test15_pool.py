#!/usr/bin/python
# -*- coding:utf-8 -*-
# 池(pool)是一个为处理数量变化并且需要限制并发的greenlet而设计的结构。 在需要并行地做很多受限于网络和IO的任务时常常需要用到它。

import gevent
from greenlet import greenlet
from gevent.pool import Pool

pool = Pool(2)


def hello_from(n):
    print('Size of pool %s' % len(pool))


pool.map(hello_from, xrange(3))


# 当构造gevent驱动的服务时，经常会将围绕一个池结构的整个服务作为中心。 一个例子就是在各个socket上轮询的类。

class SocketPool(object):
    def __init__(self):
        self.pool = Pool(1000)

    @staticmethod
    def listen(socket):
        while True:
            socket.recv()

    def add_handler(self, socket):
        if self.pool.full():
            raise Exception("At maximum pool size")
        else:
            self.pool.spawn(self.listen, socket)

    def shutdown(self):
        self.pool.kill()


sp = SocketPool()
