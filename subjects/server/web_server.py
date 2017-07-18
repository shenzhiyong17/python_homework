#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.17

import sys
import web
from web.wsgiserver import CherryPyWSGIServer
from common.IOHelper import *


class Hello:
    def GET(self, path):
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Access-Control-Allow-Origin', 'http://s.miwifi.com')
        i = web.input(name=None, cmd=None, info=None, appId=None)
        client_ip = web.ctx.ip
        path = '/%s' % path
        cfg_file = None
        result = None
        try:
            if i.appId:
                if i.appId == '2882303761517410304':    # ebit
                    cfg_file = '%s%s' % (project_dir, '/test_ebit/response_cfg/response')
                    cfg = load_config(cfg_file)
                    result = cfg[path]
                    if path.find("feature_plugin_control"):
                        result = result[i.info]
                elif i.appId == '2882303761517555697':  # ccgame
                    cfg_file = '%s%s' % (project_dir, '/test_ccgame/response_cfg/response')
                    cfg = load_config(cfg_file)
                    result = cfg[path]
                    if path == "/api-third-party/service/internal/ccgame":
                        result = result[i.cmd]
                elif i.appId == '2882303761517584655':  # ipv6
                    cfg_file = '%s%s' % (project_dir, '/ipv6/response_cfg/response')
                    cfg = load_config(cfg_file)
                    result = cfg[path]
                    if path == "/api-third-party/service/internal/ipv6":
                        result = result[i.cmd]
        except Exception as e:
            print e
            return json.dumps({'msg': 'path not found!'}, ensure_ascii=False)

        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    project_dir = '/home/szy/qos/thrift_code/localtest'

    urls = (
        '/(.*)', 'Hello',
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
