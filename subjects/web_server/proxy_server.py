#!/usr/bin/python
# -*- coding:utf-8 -*-
# 2017.07.27

import sys
import os
import re
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


def proxy(method, request, debug=False):
    url = request.url if method.lower() == 'get' else request.base_url
    data = request.get_data()
    cookies = request.cookies
    if debug:
        print 'fullpath: ', request.full_path
        print 'base_url: ', request.base_url
        print 'data: ', data

    cookie_string = ''
    if cookies:
        for ck in cookies:
            cookie_string += '%s=%s,' % (ck.encode('utf-8'), cookies[ck].encode('utf-8'))
    if debug:
        print 'cookie_string: ', cookie_string

    req = urllib2.Request(url)
    req.add_header('Host', request.host)
    req.add_header('User-Agent', request.user_agent)
    req.add_header('cookie', cookie_string.rstrip(';'))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    resp = opener.open(req, data)
    response = resp.read()
    return response
