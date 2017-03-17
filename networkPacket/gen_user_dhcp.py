#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2015.11.26

import binascii
import json
from scapy.all import *

import IOHelper
import thrift_code.sys_api.xq_conf as xq_conf


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
    except Exception as e:
        raise


def load_config(config_file_path):
    return json.loads(IOHelper.ReadContent(config_file_path))


def save_config(config_file_path, cfg):
    return IOHelper.WriteContentAndSave(config_file_path, json.dumps(cfg), 'w')


class GenUserDhcp:
    lease_file = os.curdir + '/dhcp.lease'
    ping_server = xq_conf.nginx_server['ip']
    eth = Ether()

    ip_group = {}  # { ip: mac }  # 维护的 ip-mac 表
    arp_request_list = {}  # { ip: (dstip, dsthw), }  # 收到arp请求 但是还没回应的
    maclist = {}  # { mac: hostname }
    ping_status = False
    ping_switch = False

    def __init__(self, maclist, lan_iface=None):
        self.maclist = maclist
        self.lease = self.load_lease()  # {mac: (ip, timestamp) }  # 获取到的ip 记录到文件中，租期到期前续用上次ip。

        if lan_iface is None or lan_iface == '':
            lan_iface = xq_conf.local_pc['lan_dev']

        self.lan_iface = lan_iface

    def arp_reply(self, request):
        ip = request[ARP].pdst
        srcip = ip
        dstip = request[ARP].psrc
        hwsrc = self.ip_group[ip]
        hwdst = request[Ether].src
        eth = Ether(src=hwsrc, dst=hwdst)
        arp = ARP(psrc=srcip, pdst=dstip, hwsrc=hwsrc, hwdst=hwdst)
        arp.op = "is-at"
        pkt = eth / arp
        print "====================sending a arp reply :"
        print pkt.summary()
        sendp(pkt, iface=self.lan_iface, verbose=False)

    def arp_monitor(self, verbose=True):
        while True:
            rcv = sniff(count=1, iface=self.lan_iface, filter='arp or udp port 67 or port 68')[
                0]  # 67 request, 68 reply
            try:
                # DHCP
                if isinstance(rcv.getlayer(1), IP):
                    if isinstance(rcv.getlayer(4), DHCP):  # ether/ip/udp/bootp/dhcp
                        if ('message-type', 2) in rcv[DHCP].options:  # dhcp Offer
                            print 'receive a dhcp offer'
                            print rcv.summary()
                            ip = rcv[BOOTP].yiaddr  # offer ip
                            mac = rcv[Ether].dst  # applicant mac
                            self.ip_group[ip] = mac
                            if ip in self.arp_request_list:  # arp reply
                                tmp = Ether(src=rcv[Ether].src) / ARP(pdst=ip, psrc=rcv[IP].src)
                                self.arp_reply(request=tmp)
                                del self.arp_request_list[ip]
                            hostname = self.maclist.setdefault(mac.upper(), 'vm')
                            print hostname
                            self.dhcp_requset(mac=self.ip_group[ip], requestIP=ip, hostname=hostname)  # dhcp request
                            self.save_lease(mac=mac, ip=ip)
                        elif ('message-type', 1) in rcv[DHCP].options:  # dhcp discover
                            print 'receive a dhcp discover'
                            print rcv.summary()
                # ARP
                if isinstance(rcv.getlayer(1), ARP):
                    if rcv[ARP].op == 1:  # arp requset
                        print 'receive arp request'
                        print rcv.summary()
                        print 'ip_group: ', self.ip_group
                        print 'arp_request_list.keys: ', self.arp_request_list.keys()
                        ip = rcv[ARP].pdst
                        if ip in self.ip_group:  # arp reply
                            self.arp_reply(request=rcv)
                        elif ip in self.lease:
                            print "lease has ip %s" % ip
                            mac, timestamp = self.lease[ip]
                            self.ip_group[ip] = mac
                            if mac.upper() in self.maclist.keys():
                                nowtime = time.time()
                                if nowtime - timestamp < 60 * 60 * 24:
                                    self.arp_reply(request=rcv)
                        else:
                            self.arp_request_list[ip] = (rcv[ARP].psrc, rcv[Ether].src)
            except:
                raise
            finally:
                for ip in self.arp_request_list.keys():
                    if ip in self.ip_group:
                        tmp = self.arp_request_list[ip]
                        eth = Ether(src=self.ip_group[ip], dst=tmp[1])
                        arp = ARP(psrc=ip, pdst=tmp[0], hwsrc=self.ip_group[ip], hwdst=tmp[1])
                        arp.op = 'is-at'
                        pkt = eth / arp
                        print '----------------------sending a arp reply '
                        print pkt.summary()
                        sendp(pkt, iface=self.lan_iface)
                        del self.arp_request_list[ip]

    def range_ping(self, server=xq_conf.nginx_server['ip'], interval=1, count=5, payload=10, verbose=False):
        gateway = get_gateway_ip()
        gwhw = get_gateway_hw(gateway)
        self.stop_ping()
        eth = Ether()
        ip = IP()
        icmp = ICMP()
        if payload:
            ip.len = payload + 28
            payload = 'a' * payload
            icmp_packet = eth / ip / icmp / payload
        else:
            icmp_packet = eth / ip / icmp
        icmp_packet[IP].dst = server
        icmp_packet[Ether].dst = gwhw
        if verbose: icmp_packet.show()
        self.ping_switch = True
        self.ping_status = True
        while self.ping_switch:
            for ipsrc in self.ip_group.keys():
                icmp_packet[Ether].src = self.ip_group[ipsrc]
                icmp_packet[IP].src = ipsrc
                print icmp_packet.summary()
                sendp(icmp_packet, iface=self.lan_iface, count=count, verbose=verbose)
            time.sleep(interval)
        self.ping_status = False

    def stop_ping(self):
        if self.ping_status:
            self.ping_switch = False
            while self.ping_status:
                time.sleep(1)
            print "#####  icmp request sending stopped  #####"

    # @staticmethod
    # def send(package, keep=False, count=1, interval=0, verbose=True):
    #     # package.show()
    #     ip = package.getlayer(IP)
    #     if ip:
    #         src = ip.src
    #         dst = ip.dst
    #     else:
    #         arp = package.getlayer(ARP)
    #         src = arp.psrc
    #         dst = arp.pdst
    #     while True:
    #         if verbose:
    #             print "sending a packet from %s to %s" % (src, dst)
    #         sendp(package, verbose=False)
    #         if not keep:
    #             break
    #         if count > 0:
    #             count -= 1
    #         if count == 0:
    #             break
    #         time.sleep(interval)

    def dhcp_requset(self, mac, hostname, requestIP=None):
        eth = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff')
        ip = IP(src='0.0.0.0', dst='255.255.255.255')
        udp = UDP(sport='bootpc', dport='bootps')
        tt = trans_mac(mac)
        bootp = BOOTP(op='BOOTREQUEST', chaddr=tt)

        op = []
        op.append(('client_id', '\x01' + tt))
        if requestIP:
            op.append(('message-type', 3))  # request
            op.append(('requested_addr', requestIP))
        else:
            op.append(('message-type', 1))  # discover
        op.append(('hostname', hostname))
        op.append(('vendor_class_id', 'MSFT 5.0'))
        dhcp = DHCP(options=op)

        pkt = eth / ip / udp / bootp / dhcp
        sendp(pkt, iface=self.lan_iface, verbose=False)

    def load_lease(self):
        old_lease = load_config(self.lease_file)
        if not old_lease:
            old_lease = {}
        curr_lease = {}
        nowtime = time.time()
        for ip in old_lease:
            if nowtime - old_lease[ip][1] < 60 * 60 * 24:
                curr_lease[ip] = old_lease[ip]
        return curr_lease

    def save_lease(self, mac, ip):
        timestamp = time.time()
        self.lease[ip] = (mac, timestamp)
        save_config(self.lease_file, self.lease)

    def gen_device(self, mac, hostname):
        mac_list = [{mac: hostname}]
        self.maclist = mac_list
        thread.start_new_thread(self.arp_monitor, ())
        time.sleep(1)

        self.dhcp_requset(mac=mac, hostname=hostname)
        time.sleep(1)

        self.range_ping()


def main(basemac, num, basehostname):
    maclist = gen_maclist(basemac=basemac, num=num, basehostname=basehostname)
    for mac in maclist:
        print mac

    print 'maclist.keys: ', maclist.keys()
    t = GenUserDhcp(maclist)
    thread.start_new_thread(t.arp_monitor, ())
    time.sleep(1)
    for mac in maclist.keys():
        t.dhcp_requset(mac=mac, hostname=maclist[mac])
        time.sleep(1)
    t.range_ping()


if __name__ == '__main__':
    main(basemac='68:F7:28:40:79:01', num=5, basehostname='ho')
