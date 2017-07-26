#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.17

import sys
import web
import urllib2
from web.wsgiserver import CherryPyWSGIServer
from common.IOHelper import *


class Hello:
    def GET(self, path):
        i = web.input(name=None, cmd=None, info=None, appId=None)
        path = '/%s' % path
        result = None
        try:
            if i.appId:
                web.header('Access-Control-Allow-Credentials', 'true')
                web.header('Access-Control-Allow-Origin', 'http://s.miwifi.com')
                if i.appId == '2882303761517410304':  # ebit
                    cfg_file = '%s%s' % (project_dir, '/test_ebit/response_cfg/response')
                    cfg = load_config(cfg_file)
                    result = cfg[path]
                    print '--------------- result: %s' %result
                    if path.endswith("feature_plugin_control"):
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
            else:
                print "web.ctx.ip:%s" % web.ctx.ip  # client ip
                print "web.ctx.host: %s" % web.ctx.host  # www.163.com
                print "web.ctx.home: %s" % web.ctx.home  # http://www.163.com
                print "web.ctx.homedomain: %s" % web.ctx.homedomain  # http://www.163.com
                print "web.ctx.homepath: %s" % web.ctx.homepath  #
                print "web.ctx.status: %s" % web.ctx.status  # 200 OK
                print "web.ctx.headers: %s" % web.ctx.headers  # [('Access-Control-Allow-Credentials', 'true'), ('Access-Control-Allow-Origin', 'http://s.miwifi.com')]
                print "web.ctx.method: %s" % web.ctx.method  # GET
                print "web.ctx.query: %s" % web.ctx.query  # ?callback=latestInstantNews&d=1231
                print "web.ctx.fullpath: %s" % web.ctx.fullpath  # /special/00774IVV/hot_pop_js2017.js?callback=latestInstantNews&d=1231
                print "web.ctx.env: "
                for ver in web.ctx.env:
                    print "\t%s: %s" %(ver, web.ctx.env.get(ver))
                print web.ctx.env.get('HTTP_REFERER', 'http://google.com')
                url = "%s%s" % (web.ctx.home, web.ctx.fullpath)
                return urllib2.urlopen(url).read()
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
