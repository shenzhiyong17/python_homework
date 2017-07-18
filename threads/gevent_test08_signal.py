#!/usr/bin/python
# -*- coding:utf-8 -*-
# 接收signal 信号做相应处理

import gevent
import signal


def run_forever():
    print('running..')
    gevent.sleep(1000)


def handler_sigquit():
    print ('Got SIGQUIT')
    gevent.kill(gevent.getcurrent())
    gevent.sleep(0)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, handler_sigquit)
    thread = gevent.spawn(run_forever)
    thread.join()