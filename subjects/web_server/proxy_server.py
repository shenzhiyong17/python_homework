#!/usr/bin/python
# -*- coding:utf-8 -*-
# 2017.07.27

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


def proxy(method, request):
    data = request.data if request.data else None
    print 'data: ', request.data
    print 'cookies: ', request.cookies
    cookies = request.cookies
    cookie_string = ''
    cookie_header = {}
    if cookies:
        for ck in cookies:
            cookie_string += '%s=%s;' %(ck, cookies[ck])
        cookie_header = {'Cookie': cookie_string.rstrip(';')}

    if method.lower() == 'get':
        req = urllib2.Request(url=request.url, headers=cookie_header)
        result = urllib2.urlopen(req).read()
        # result = urllib2.urlopen(request.url, data).read()
        print result[:200]
        return result
    elif method.lower() == 'post':
        url = request.url
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        # enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()
