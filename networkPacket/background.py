#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# latency.py -s -p PORT
# latency.py -c -h IP -p PORT

import getopt
import sys
import os
import select
import socket
import traceback
import datetime
import time
import gevent
from gevent import monkey
from gevent.server import DatagramServer
from gevent.server import StreamServer

monkey.patch_all()

is_server = False
port = '12345'
host = ''
client_number = 10
interval = 0.001
long_pkt = '.' * 1400
short_pkt = '.'

up_test_pkt = 'u' * 1400
down_test_pkt = 'd'
both_test_pkt = 'b' * 1400

direction = 0
pkt_type = 'tcp'


def usage(err=None):
    intro = \
        """
        usage:
            background.py -s -u/-t -p PORT                              #work as server
            background.py -c -u/-t -n NUM -h IP -p PORT -d 0/1/2        #work as client

                -c          work as client
                -s          work as server
                -u          UDP
                -t          TCP, as default
                -d 0/1/2    flow type, 0 down/1 up/2 both, control the pkt-lens, default=0 down-test
                -h IP       server-ip
                -p PORT     default=12345
                -n NUM      clients number, default = 10
                -i interval client send interval, defalut = 0.001

        """
    if err:
        print "Err: " + err
    else:
        print intro
    sys.exit(1)


class UDPServer(DatagramServer):
    def handle(self, data, address):
        if data[0] == 'u':  # upload test
            self.socket.sendto(short_pkt, address)
        elif data[0] == 'd':  # download test
            self.socket.sendto(long_pkt, address)
        else:  # both test
            for i in xrange(8):
                self.socket.sendto(long_pkt, address)


class TCPServer(StreamServer):
    def handle(self, socket, address):
        print 'client connected. ', address
        try:
            while True:
                data = socket.recv(2048)
                # print 'recv 1.'
                if data:
                    if data[0] == 'u':
                        socket.send(short_pkt)
                    elif data[0] == 'd':
                        socket.send(long_pkt)
                    else:
                        for i in xrange(8):
                            socket.send(long_pkt)
                else:
                    break
        except Exception, ex:
            print ex
        finally:
            socket.close()
            print 'client exited.', address


def server_work(port):
    if pkt_type == 'udp':
        server = UDPServer(':' + port)
    else:
        server = TCPServer(':' + port)
    server.serve_forever()


class Client:
    def __init__(self, cli_id, cli_type, host, port, interval):
        self.host = host
        self.port = port
        self.sent_cnt = 0
        self.recv_cnt = 0
        self.cli_id = cli_id
        self.interval = interval
        if cli_type == 'udp':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((host, port))

    def run(self):
        try:
            while True:
                r, w, _ = select.select([self.socket], [], [], self.interval)  # 非阻塞IO
                if not r:  # 没有收到包就，继续发
                    self.sent_cnt += 1
                    if direction == 1:
                        self.socket.sendall(up_test_pkt)
                    elif direction == 0:
                        self.socket.sendall(down_test_pkt)
                    else:
                        self.socket.sendall(both_test_pkt)

                        # print 'sent 1.'
                else:  # 收到包就记个数
                    for _r in r:
                        _r.recv(2048)
                        self.recv_cnt += 1
                        # print 'recv 1.'
        except:
            traceback.print_exc()
        finally:
            print 'client ', self.cli_id, 'end.'
            self.socket.close()


def client_worker(id, pkt_type, host, port, interval):
    cli = Client(id, pkt_type, host, port, interval)
    cli.run()


def main():
    global is_server, port, host, client_number, direction, pkt_type, interval
    try:
        opts, args = getopt.getopt(sys.argv[1:], "csn:p:h:tud:i:", [])

        for opt, arg in opts:
            if opt in ("-s",):
                is_server = True
            elif opt in ("-c",):
                is_server = False
            elif opt in ("-p",):
                port = arg
            elif opt in ("-h",):
                host = arg
            elif opt in ("-n",):
                client_number = int(arg)
            elif opt in ("-t",):
                pkt_type = "tcp"
            elif opt in ("-u",):
                pkt_type = "udp"
            elif opt in ("-d",):
                direction = int(arg)
            elif opt in ("-i",):
                interval = float(arg)
            else:
                usage()

        if is_server:
            if port <= 0:
                usage('port cannot be NULL for server.')

            print "work as server, listen on port: ", str(port)
            server_work(port)

        else:
            if port <= 0 or host == '':
                usage('port and host cannot be NULL for client.')

            print "work as client, connect to host: ", host, ", port: ", str(port)
            clients = []
            for i in xrange(client_number):
                print 'spawn client', i, 'to setup flow.'
                clients.append(gevent.spawn(client_worker, i, pkt_type, host, port, interval))

            gevent.joinall(clients)

    except Exception, e:
        print e
    pass


if __name__ == '__main__':
    main()
