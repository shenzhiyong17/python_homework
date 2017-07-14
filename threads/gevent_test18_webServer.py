#!/usr/bin/python
# -*- coding:utf-8 -*-
# 很多集成了gevent的web框架将HTTP会话对象以线程局部变量的方式存储在gevent内。
# 例如使用Werkzeug实用库和它的proxy对象，我们可以创建Flask风格的请求对象。

from gevent.local import local
from werkzeug.local import LocalProxy
from werkzeug.wrappers import Request
from contextlib import contextmanager

from gevent.wsgi import WSGIServer

_requests = local()
request = LocalProxy(lambda: _requests.request)


@contextmanager
def sessionmanager(environ):
    for key in environ:
        print key, environ[key]
    _requests.request = Request(environ)
    yield
    _requests.request = None


def logic():
    print '-------------------------'
    for property in dir(request):
        print property
    print '-------------------------'
    return "Hello " + request.remote_addr


def application(environ, start_response):
    status = '200 OK'

    with sessionmanager(environ):
        body = logic()

    headers = [
        ('Content-Type', 'text/html')
    ]

    start_response(status, headers)
    return [body]


WSGIServer(('192.168.31.106', 8000), application).serve_forever()
