#!/usr/bin/python
# date : 2015-10-20
# author: szy

import os
import re
import thread
import time
from scapy.all import *


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


'''
def icmp_request(dstip,srcip,hwsrc="b8:ca:3a:af:b9:c5",payload=0,interval=0,keep=False,verbose=False):
    hwdst = get_gateway_hw(get_gateway_ip())
    eth = Ether(src=hwsrc,dst=hwdst)
    ip = IP(dst=dstip,src=srcip,len=payload+28)
    icmp = ICMP(type=8)
    payload = 't'*payload
    icmp_packet = eth/ip/icmp/payload
    if verbose:
        icmp_packet.show()
    while True:
        if verbose:
            print "sending a icmp request from " + srcip + " to " + dstip
            print "---------------------------------"
        sendp(icmp_packet)
        if interval != 0:
            time.sleep(interval)
        if keep == False : break
'''


def icmp_request(kwargs):
    kwargs.setdefault('dstip', '10.10.101.81')
    kwargs.setdefault('srcip', '192.168.1.206')
    kwargs.setdefault('hwsrc', 'b8:ca:3a:af:b9:c5')
    kwargs.setdefault('payload', 0)
    kwargs.setdefault('interval', 0)
    kwargs.setdefault('keep', False)
    kwargs.setdefault('verbose', False)

    dstip = kwargs['dstip']
    srcip = kwargs['srcip']
    payload = kwargs['payload']
    interval = kwargs['interval']
    verbose = kwargs['verbose']

    hwdst = get_gateway_hw(get_gateway_ip())
    eth = Ether(src=kwargs['hwsrc'], dst=hwdst)
    ip = IP(dst=dstip, src=srcip, len=payload + 28)
    icmp = ICMP(type=8)
    payload = 't' * payload
    icmp_packet = eth / ip / icmp / payload
    if verbose:
        icmp_packet.show()
    while True:
        if verbose:
            print "sending a icmp request from " + srcip + " to " + dstip
            print "---------------------------------"
        sendp(icmp_packet)
        if interval != 0:
            time.sleep(interval)
        if kwargs['keep'] == False: break


def icmp_sniff():
    while True:
        pkt = sniff(count=5, filter='icmp and dst 192.168.31.206')
        try:
            pkt[0].show()
        except:
            pass
            # finally:
            #     time.sleep(3)


'''
def arp_request(hwsrc="b8:ca:3a:af:b9:c5", hwdst="00:00:00:00:00:00", srcip="192.168.31.200", dstip="192.168.31.1",verbose=False):
    eth = Ether(src=hwsrc, dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(psrc=srcip, pdst=dstip, hwsrc=hwsrc, hwdst=hwdst)
    arp.op = "who-has"  ## arp.op = 1
    pkt = eth / arp
    while True:
        if verbose == True :
            print "sending a arp request ..."
            pkt.show()
            print "---------------------------"
        sendp(pkt)
        time.sleep(10)
'''


def arp_reply(ip_group, verbose=False):
    while True:
        pkts = sniff(count=1, filter='arp')
        rcv = pkts[0]
        try:
            if rcv[ARP].op == 1 and ip_group.has_key(rcv[ARP].pdst):
                srcip = rcv[ARP].pdst
                dstip = rcv[ARP].psrc
                hwsrc = ip_group[srcip]
                hwdst = rcv[Ether].src
                if verbose == True:
                    print "receive a arp requset packet ..."
                    rcv.show()
                    print "--------------------------------"

                eth = Ether(src=hwsrc, dst=hwdst)
                arp = ARP(psrc=srcip, pdst=dstip, hwsrc=hwsrc, hwdst=hwdst)
                arp.op = "is-at"
                pkt = eth / arp
                if verbose == True:
                    print "sending a arp replay packet ..."
                    pkt.show()
                    print "-------------------------------"
                sendp(pkt)
        except:
            pass


def gen_user(number):
    base_mac = "b8:ca:3a:ff:99:01";
    base_ip = "192.168.1.20";
    split_ip = base_ip.split(".");
    split_mac = base_mac.split(":");
    ip_group = {};
    for i in range(number):
        ip = ".".join(split_ip[0:-1] + [str(int(split_ip[-1]) + i)]);
        mac = ":".join(split_mac[0:-1] + [str(int(split_mac[-1]) + i)]);
        ip_group[ip] = mac;
        thread.start_new_thread(icmp_request,
                                ({'hwsrc': mac, 'srcip': ip, 'payload': 500, 'interval': 2, 'keep': True},))
    arp_reply(ip_group, verbose=False)


if __name__ == "__main__":
    if os.geteuid():
        args = [sys.executable] + sys.argv
        os.execlp('sudo', *args)
    gen_user(5)
