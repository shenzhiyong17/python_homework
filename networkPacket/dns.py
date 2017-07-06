#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.06

import random
from scapy.all import *
from networkPacket.process_net import *
from common.network_config import NetworkConfig


class DnsQuery:
    router = NetworkConfig.router['br-lan_ip']
    dst_mac = get_gateway_hw(router)

    def query(self, domain, ns=None, ipv6=False):
        if not ns:
            ns = NetworkConfig.local_pc['dns_server']
        eth = Ether()
        ip = IP(dst=ns, src=NetworkConfig.local_pc['lan1']['ip'])
        udp = UDP(dport=53, sport=random.randint(20000, 50000))
        dns = DNS()
        dns.qr = 0  #1为响应，0为查询
        dns.opcode = 0  #查询或响应的类型（若为0则表示是标准的，若为1则是反向的，若为2则是服务器状态请求）
        dns.tc = 0  #截断标志位。1表示响应已超过512字节并已被截断,by default
        dns.rd = 1  #该位为1表示客户端希望得到递归回答
        dns.qdcount = 1 #问题数
        dns.ancount = 0 #资源记录数
        dns.nscount = 0 #授权资源记录数
        dns.arcount = 0 #额外资源记录数
        dns.qd = DNSQR()
        dns.qd.qname = domain
        dns.qd.qtype = 'AAAA' if ipv6 else 'A'
        dns.qd.qclass = 1   # IN(0x0001)

        pkt = eth / ip / udp / dns
        pkt.show()
        sendp(pkt, iface='eno1', count=1, verbose=True)


if __name__ == '__main__':
    # rcv = sniff(count=4, iface='eno1', filter='udp port 53')
    # for pkt in rcv:
    #     print pkt.summary()
    #     print '-------------------------'
    #     pkt.show()
    #     print '========================='

    dns = DnsQuery()
    dns.query('www.163.com',ipv6=True)
