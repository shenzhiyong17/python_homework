#!/usr/bin/python
# -*- coding:utf-8 -*-
# 子进程

import gevent
from gevent.subprocess import Popen, PIPE


def cron():
    while True:
        print("cron")
        gevent.sleep(2)


g = gevent.spawn(cron)  # 开始运行
sub = Popen(['sleep 1; uname'], stdout=PIPE, shell=True)    # 开始运行
gevent.sleep(10)
out, err = sub.communicate()    # 获得输出
g.kill()
print(out.rstrip())
