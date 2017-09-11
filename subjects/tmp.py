#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64
import urllib
import hashlib

print urllib.unquote('1%2B1000%2B3')
print base64.b64decode('56e4c455635a39d42e08b8cd31a1c4ec72f21877')


def gen_key(channel_secret, nonce):
    sh = hashlib.sha256()
    sh.update(base64.b64decode(channel_secret) + base64.b64decode(nonce))
    return base64.b64encode(sh.digest())

channel_secret = 'YQkdV/JZMnOfvT5oeJecUoWDIH7ilkVLg1uBAamaFmo='
nonce = 'DB6KUxVNCjCseacF'
print gen_key(channel_secret, nonce)
print base64.b64encode(hashlib.sha256(base64.b64decode(channel_secret) + base64.b64decode(nonce)).digest())
