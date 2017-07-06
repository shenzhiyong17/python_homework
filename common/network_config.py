#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.06.22


class NetworkConfig():
    nginx_server = {
        'ip': '10.231.39.173'
    }

    local_pc = {
        'lan1': {
            'dev': 'eno1',
            'ip': '192.168.31.106',
            'mac': 'b8:ca:3a:af:b9:b4',
        },
        'lan2': {
            'dev': 'enp1s0',
            'ip': '172.16.101.201',
            'mac': '00:e0:4c:68:01:12',
        },
        'dns_server': '192.168.31.1',
        'gateway': '192.168.31.1'
    }

    router = {
        'wan_ip': '',
        'br-lan_ip': '192.168.31.1',
        'br-lan_mac': 'f0:b4:29:83:6d:da',
    }
