#!/usr/bin/python
# -*- coding:utf-8 -*-
# 把阻塞变为非阻塞的协程

from gevent import monkey
import socket
import select

print(socket.socket)
print "After monkey patch"
monkey.patch_socket()
print(socket.socket)

# --
print select.select
monkey.patch_select()
print "After monkey patch"
print(select.select)
