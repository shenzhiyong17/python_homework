#!/usr/bin/python
# -*- coding:utf-8 -*-
# 接收signal 信号做相应处理

import gevent
import signal


def run_forever():
    gevent.sleep(1000)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, gevent.kill)
    thread = gevent.spawn(run_forever)
    thread.join()