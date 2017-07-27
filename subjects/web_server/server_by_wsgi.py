#!/usr/bin/python
# -*- coding:utf-8 -*-
# 很多集成了gevent的web框架将HTTP会话对象以线程局部变量的方式存储在gevent内。
# 例如使用Werkzeug实用库和它的proxy对象，我们可以创建Flask风格的请求对象。

import sys
import os
from gevent.local import local
from werkzeug.local import LocalProxy
from werkzeug.wrappers import Request
from contextlib import contextmanager
import urllib2
import urllib
import json
import base64
from common.Encrypt import AESCipher, encrypt, gen_key
from gevent.wsgi import WSGIServer
from thrift_code.tool.IOHelper import load_config
from urlparse import parse_qs
from proxy_server import proxy

_requests = local()
request = LocalProxy(lambda: _requests.request)


@contextmanager
def sessionmanager(environ):
    _requests.request = Request(environ)
    yield
    _requests.request = None


def logic(environ, debug=False):
    if debug:
        print '============== begin ================'
        print 'url: ', request.url
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    query_string = environ['QUERY_STRING']
    querys = {}
    result = ''
    hit = False
    if query_string:
        for query in query_string.split('&'):
            k, v = query.split('=', 1)
            querys[k] = v
    try:
        if method == 'GET':
            if querys.get('appId') == '2882303761517410304' or path.find('tianyi') > -1:  # ebit
                cfg_file = '%s%s' % (project_dir, '/test_ebit/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg.get(path, None)
                if path.find("feature_plugin_control") > -1:
                    result = result[urllib.unquote(querys['info'])]
                    print 'info: ', type(querys['info']), querys['info']
            elif querys.get('appId') == '2882303761517555697' or path.find('ccgame') > -1:  # ccgame
                cfg_file = '%s%s' % (project_dir, '/test_ccgame/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg[path]
                if path == "/api-third-party/service/internal/ccgame":
                    result = result[urllib.unquote(querys['cmd'])]
            elif querys.get('appId') == '2882303761517584655' or path.find('ipv6') > -1:  # ipv6
                cfg_file = '%s%s' % (project_dir, '/ipv6/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg[path]
                if path == "/api-third-party/service/internal/ipv6":
                    result = result[urllib.unquote(querys['cmd'])]

            if result:
                # 命中配置
                hit = True
                result = json.dumps(result, ensure_ascii=False).encode('utf-8')
                if debug:
                    print 'result: ', result
            else:
                # proxy
                result = proxy('GET', request).encode('utf-8')
            if querys.get('nonce'):
                if debug:
                    print 'nonce: ', querys['nonce']
                channel_secret = get_channel_secret()
                encrypt_key = gen_key(channel_secret, urllib.unquote(querys['nonce']))[:16]
                if debug:
                    print 'encrypt_key: ', encrypt_key
                result = encrypt(encrypt_key, result)
                if debug:
                    print 'encrypt result: ', result

        elif method == 'POST':
            result = proxy('POST', request)

    except Exception as e:
        print e
    return result, hit


def application(environ, start_response):
    status = '200 OK'

    with sessionmanager(environ):
        body, hit = logic(environ, debug=True)
        print 'body type: ', type(body), body
        print 'hit: ', hit
        print '=================== end ===================='

    headers = [
        ('Content-Type', 'text/html'),
    ]
    if hit:
        headers += [
            ('Access-Control-Allow-Origin', 'http://s.miwifi.com'),
            ('Access-Control-Allow-Credentials', 'true')
        ]

    start_response(status, headers)
    return body


def get_channel_secret():
    cmd = "uci get messaging.deviceInfo.CHANNEL_SECRET"
    return "yabUeoFU+C8Rg9wTlUyuRM9mQAj8bM9XNVmFY/oOFVA="


def main():
    listener = sys.argv[1]
    ssl_args = {}
    if len(sys.argv) > 2:
        if int(sys.argv[2]) == 1:
            ssl_args['keyfile'] = "/ssl_key/nginx_nopwd.key"
            ssl_args['certfile'] = "/ssl_key/nginx.crt"
    WSGIServer(listener=listener, application=application, **ssl_args).serve_forever()


if __name__ == '__main__':
    project_dir = '/home/szy/qos/thrift_code/localtest'
    main()
