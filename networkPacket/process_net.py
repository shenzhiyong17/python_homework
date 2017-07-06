#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.06

import os
import re
import json
import binascii
from common.IOHelper import *

def get_gateway_ip():
    t = os.popen('route -n')
    for i in t:
        if i.startswith('0.0.0.0'):
            r = re.split("\s+", i)
            return r[1]


def get_gateway_hw(ip):
    t = os.popen('arp -en %s' % ip)
    for i in t:
        if i.startswith(ip):
            r = re.split("\s+", i)
            return r[2]


def gen_maclist(basemac, num, basehostname):
    # maclist = { mac:hostname }
    maclist = {}
    split_mac = basemac.split(':')
    for i in range(num):
        last = "%02X" % (int(split_mac[-1]) + i)
        maclist[":".join((split_mac[0:-1]) + [last])] = basehostname + str(i)
    return maclist


def trans_mac(mac):
    # string to hex.
    try:
        res = ''
        tmp = mac.split(':')
        for i in tmp:
            res += binascii.a2b_hex(i)
        return res
    except Exception as exc:
        raise exc


def load_config(config_file_path):
    return json.loads(ReadContent(config_file_path))


def save_config(config_file_path, cfg):
    return WriteContentAndSave(config_file_path, json.dumps(cfg), 'w')