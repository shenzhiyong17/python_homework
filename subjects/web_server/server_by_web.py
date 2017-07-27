#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.17

import sys
import web
import hashlib
import base64
import urllib2
import urllib
from thrift_code.tool.commonHelper import AESCipher
from web.wsgiserver import CherryPyWSGIServer
from thrift_code.tool.IOHelper import *
from thrift_code.sys_api.telnet_cmd import telnet_cmd


class ApiThirdParty:
    def GET(self, path):
        i = web.input(name=None, cmd=None, info=None, appId=None, nonce=None)
        # client_ip = web.ctx.ip
        path = '/%s' % path
        result = None
        try:
            if path.find('tianyi') > -1:  # ebit
                cfg_file = '%s%s' % (project_dir, '/test_ebit/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg[path]
                if path.find("feature_plugin_control") > -1:
                    result = result[i.info]
            elif path.find('ccgame') > -1:  # ccgame
                cfg_file = '%s%s' % (project_dir, '/test_ccgame/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg[path]
                if path == "/api-third-party/service/internal/ccgame":
                    result = result[i.cmd]
            elif path.find('ipv6') > -1:  # ipv6
                cfg_file = '%s%s' % (project_dir, '/ipv6/response_cfg/response')
                cfg = load_config(cfg_file)
                result = cfg[path]
                if path == "/api-third-party/service/internal/ipv6":
                    result = result[i.cmd]

            if result is not None:  # hit
                web.header('Access-Control-Allow-Credentials', 'true')
                web.header('Access-Control-Allow-Origin', 'http://s.miwifi.com')
                result = json.dumps(result, ensure_ascii=False)
            else:  # proxy
                url = '%s%s' % (web.ctx.homedomain, web.ctx.fullpath)
                result = urllib2.urlopen(url).read()

        except Exception as e:
            print e
            return json.dumps({'msg': 'path not found!'}, ensure_ascii=False)

        if i.nonce:
            channel_secret = get_channel_secret()
            encrypt_key = gen_key(channel_secret, i.nonce)[:16]
            result = encrypt(encrypt_key, result.encode('utf-8'))

        return result

    def POST(self, path):
        url = '%s%s' % (web.ctx.homedomain, web.ctx.fullpath)
        data = dict(web.input())
        print url, data
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        # enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()


def get_channel_secret():
    cmd = "uci get messaging.deviceInfo.CHANNEL_SECRET"
    return "yabUeoFU+C8Rg9wTlUyuRM9mQAj8bM9XNVmFY/oOFVA="


def gen_key(channel_secret, nonce):
    sh = hashlib.sha256()
    sh.update(base64.b64decode(channel_secret) + base64.b64decode(nonce))
    return base64.b64encode(sh.digest())


def encrypt(encrypt_key, content):
    encrypt_ins = AESCipher(encrypt_key)
    return encrypt_ins.encrypt(content)


if __name__ == "__main__":
    project_dir = '/home/szy/qos/thrift_code/localtest'

    urls = (
        '/(.*)', 'ApiThirdParty',
    )

    is_https = False
    if len(sys.argv) > 2:
        if int(sys.argv[2]) == 1:
            is_https = True

    if is_https:
        CherryPyWSGIServer.ssl_certificate = "/ssl_key/nginx.crt"
        CherryPyWSGIServer.ssl_private_key = "/ssl_key/nginx_nopwd.key"

    app = web.application(urls, globals())
    app.run()
