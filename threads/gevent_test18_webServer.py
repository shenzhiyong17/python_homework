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
        print '%s = %s' % (key, environ[key])
    _requests.request = Request(environ)
    yield
    _requests.request = None


def logic(environ):
    body = environ['PATH_INFO']
    # print '-------------------------'
    # for property in dir(request):
    #     print property
    # print '-------------------------'
    # body = "<p>remote_addr: %s</p>" % request.remote_addr
    # body += "<p>args: %s</p>" % request.args.keys()
    # body += "<p>base_url: %s</p>" % request.base_url.encode()
    # body += "<p>cookies: %s</p>" % request.cookies.keys()
    # body += "<p>data: %s</p>" % request.data.encode()
    # body += "<p>date: %s</p>" % request.date
    # body += "<p>headers: %s</p>" % request.headers.keys()
    # body += "<p>User-Agent: %s</p>" %request.headers['User-Agent'].encode()
    # body += "<p>Connection: %s</p>" % request.headers['Connection'].encode()
    # body += "<p>Host: %s</p>" % request.headers['Host'].encode()
    # body += "<p>Accept: %s</p>" % request.headers['Accept'].encode()
    # body += "<p>host_url: %s</p>" % request.host_url.encode()
    # body += "<p>full_path: %s</p>" % request.full_path.encode()
    # body += "<p>method: %s</p>" % request.method.encode()
    # body += "<p>query_string: %s</p>" % request.query_string.encode()
    # body += "<p>url: %s</p>" % request.url.encode()
    return body


def application(environ, start_response):
    status = '200 OK'

    with sessionmanager(environ):
        body = logic(environ)

    headers = [
        ('Content-Type', 'text/html'),
        ('Access-Control-Allow-Origin', 'http://s.miwifi.com'),
        ('Access-Control-Allow-Credentials', 'true')
    ]

    start_response(status, headers)
    return body


if __name__ == '__main__':
    WSGIServer(('192.168.31.106', 8000), application).serve_forever()
