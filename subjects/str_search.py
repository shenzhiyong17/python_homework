#!/usr/bin/python
# -*- coding:utf-8 -*-
# 2017.08.03

import re
import urllib2
import time
from common.timing import tic


def curl(url):
    try:
        return urllib2.urlopen(url, timeout=3).read()
    except:
        return ''


def get_urls(f):
    urls = set()
    for url in re.finditer('http[s]?://[^\"|^\'|^\#)]*', f):
        urls.add(url.group().strip('/'))
    return urls


def get_domain(url):
    url = re.sub('^http[s]?://', '', url)
    url = re.sub('/.*', '', url)
    url = '.'.join(url.split('.')[-2:])
    return url


def gen_db(homepage, db=None, debug=False):
    if not db:
        db = {}
    for url in get_urls(curl(homepage)):
        if debug:
            print url
        domain = get_domain(url)
        db.setdefault(domain, []).append(url)
    return db


if __name__ == '__main__':
    _db = gen_db('http://www.run46.com')
    db = None
    for key, homepages in _db.iteritems():
        for url in homepages:
            print url
            db = gen_db(url, db, debug=False)
    for k, v in _db.iteritems():
        print k, ' : ', v
