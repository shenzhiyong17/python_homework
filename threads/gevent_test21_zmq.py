#!/usr/bin/python
# -*- coding:utf-8 -*-
# 使用gevent.socket来以非阻塞的方式 轮询ZereMQ socket
# Note: Remember to ``pip install pyzmq gevent_zeromq``

import gevent
from gevent_zeromq import zmq
# Global Context
context = zmq.Context()


def server():
    server_socket = context.socket(zmq.REQ)
    server_socket.bind("tcp://127.0.0.1:5000")
    gevent.sleep(0)

    for request in range(1, 10):
        print request
        server_socket.send("Hello")
        print('Switched to Server for %s' % request)
        # Implicit context switch occurs here
        server_socket.recv()


def client():
    client_socket = context.socket(zmq.REP)
    client_socket.connect("tcp://127.0.0.1:5000")

    for request in range(1, 10):
        client_socket.recv()
        print('Switched to Client for %s' % request)
        # Implicit context switch occurs here
        client_socket.send("World")


publisher = gevent.spawn(server)
client = gevent.spawn(client)

gevent.joinall([publisher, client])
