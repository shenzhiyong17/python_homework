#!/usr/bin/python
# -*- coding:utf-8 -*-
# 简单server
# see background.py

from gevent.server import StreamServer


# On Unix: Access with ``$ nc 127.0.0.1 5000``
# On Window: Access with ``$ telnet 127.0.0.1 5000``

def handle(socket, address):
    socket.send("Hello from a telnet!\n")
    socket.send(str(address[1]) + '\n')
    socket.close()


server = StreamServer(('127.0.0.1', 5000), handle)
server.serve_forever()
