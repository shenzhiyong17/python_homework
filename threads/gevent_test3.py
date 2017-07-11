#!/usr/bin/python
# -*- coding:utf-8 -*-

import gevent
import urllib2
import simplejson as json
import gevent.monkey

gevent.monkey.patch_socket()


def fetch(pid):
    response = urllib2.urlopen('http://10.231.39.173/client_ip.html')
    result = response.read()
    print 'Process ', pid
    return result


def synchronous():
    for i in range(1, 10):
        fetch(i)


def asynchronous():
    threads = []
    for i in range(1, 10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)


print 'Synchronous:'
synchronous()

print 'Asynchronous:'
asynchronous()
