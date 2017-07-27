#!/usr/bin/python
# -*- coding:utf-8 -*-
# 很多集成了gevent的web框架将HTTP会话对象以线程局部变量的方式存储在gevent内。
# 例如使用Werkzeug实用库和它的proxy对象，我们可以创建Flask风格的请求对象。

import sys
from gevent.local import local
from werkzeug.local import LocalProxy
from werkzeug.wrappers import Request
from contextlib import contextmanager
from gevent.wsgi import WSGIServer

_requests = local()
request = LocalProxy(lambda: _requests.request)


@contextmanager
def sessionmanager(environ):
    _requests.request = Request(environ)
    yield
    _requests.request = None


def logic(environ):
    path = environ['PATH_INFO']
    params = {}
    try:
        querys = environ['QUERY_STRING'].split('&')
        for query in querys:
            k, v = query.split('=', 1)
            params[k] = v
    except Exception as e:
        print e

    # print '-------------------------'
    # for property in dir(request):
    #     print property
    # print '-------------------------'
    return path, str(params)


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


def main():
    listener = sys.argv[1]
    ssl_args = {}
    if len(sys.argv) > 2:
        if int(sys.argv[2]) == 1:
            ssl_args['keyfile'] = "/ssl_key/nginx_nopwd.key"
            ssl_args['certfile'] = "/ssl_key/nginx.crt"
    WSGIServer(listener=listener, application=application, **ssl_args).serve_forever()


if __name__ == '__main__':
    main()
