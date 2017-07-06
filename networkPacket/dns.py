#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.07.06

import random
import threading
import time
import sys
from scapy.all import *
from networkPacket.process_net import *
from common.network_config import NetworkConfig



class DnsResolve:
    gate_way = NetworkConfig.router['br-lan_ip']
    gate_mac = get_gateway_hw(gate_way)
    lan = NetworkConfig.local_pc['lan1']
    dns_server = NetworkConfig.local_pc['dns_server']
    tmp_res = None
    stop = False

    def query(self, domain, dns_server=None, ipv6=False):
        # 发送 dns query包
        if not dns_server:
            dns_server = self.dns_server
        eth = Ether()
        ip = IP(dst=dns_server, src=self.lan['ip'])
        udp = UDP(dport=53, sport=random.randint(20000, 50000))
        dns = DNS()
        dns.qr = 0  #1为响应，0为查询
        dns.opcode = 0  #查询或响应的类型（若为0则表示是标准的，若为1则是反向的，若为2则是服务器状态请求）
        dns.tc = 0  #截断标志位。1表示响应已超过512字节并已被截断,by default
        dns.rd = 0  #该位为1表示客户端希望得到递归回答
        dns.qdcount = 1 #问题数
        dns.ancount = 0 #资源记录数
        dns.nscount = 0 #授权资源记录数
        dns.arcount = 0 #额外资源记录数
        dns.qd = DNSQR()
        dns.qd.qname = domain
        dns.qd.qtype = 'AAAA' if ipv6 else 'A'
        dns.qd.qclass = 1   # IN(0x0001)

        pkt = eth/ ip / udp / dns
        # pkt.show()
        sendp(pkt, iface=self.lan['dev'], count=1, verbose=True)

    def reslove(self, domain, dns_server=None, ipv6=False):
        # 解析域名
        def rcv():
            # 抓dns answer包，回传到 self.tmp_res，用self.stop控制线程退出
            while not self.stop:
                rcv = sniff(count=1, iface=self.lan['dev'], filter='src %s and udp and udp port 53' % dns_server, timeout=1)
                if rcv:
                    rcv = rcv[0]
                    if isinstance(rcv.getlayer(1), IP) and isinstance(rcv.getlayer(3), DNS):
                        self.tmp_res = rcv
                        return

        t = threading.Thread(target=rcv)
        t.start()
        time.sleep(0.1)
        self.query(domain=domain, dns_server=dns_server, ipv6=ipv6)
        if t.is_alive:
            t.join(timeout=3)   # 等待线程结束，超时时间为3秒
            self.stop = True    # 强制线程退出
        try:
            res = self.tmp_res[DNS][DNSRR]
        except TypeError:
            return []
        data = []
        rdlen = 16 if ipv6 else 4
        while res:
            if res.rdlen == rdlen:
                data.append(res.rdata)
            res = res.payload
        return data

if __name__ == '__main__':
    dns = DnsResolve()
    print dns.reslove('www.163.com', dns_server='119.90.39.115', ipv6=False)
