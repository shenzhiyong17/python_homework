#!/usr/bin/python
# -*- coding:utf-8 -*-

# 创建Greenlet的子类，并且重写 _run 方法

import gevent
from gevent import Greenlet


class MyGreenlet(Greenlet):

    def __init__(self, message, n):
        Greenlet.__init__(self)
        self.message = message
        self.n = n

    def _run(self):
        gevent.sleep(self.n)
        print(self.message)

g = MyGreenlet("Hi there!", 3)
g.start()
g.join()