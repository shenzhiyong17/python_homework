#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# latency.py -s -p PORT
# latency.py -c -h IP -p PORT
#


import getopt
import sys
import os
import socket
import traceback
import time
import struct
import select
import thread
from thrift_code.tool.timer import timer


def usage(err=None):
    if err:
        print "Err: " + err
    print """
usage:
    latency.py -s -p PORT                   #work as server
    latency.py -c -n NUM -h IP -p PORT      #work as client, send NUM packets per second
"""


class Delay:
    is_server = False
    host = ''
    num = 10
    total_sent_time = 0

    def server_delay(self, port):
        # 收到包后原样返回
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
            s.bind(('0.0.0.0', port))

            while True:
                count = 0
                addr = None
                while True:
                    try:
                        data, addr = s.recvfrom(1024)

                        if data == '':
                            # print 'client exit.'
                            break
                        count += 1
                        s.sendto(data, addr)
                    except Exception:
                        traceback.print_exc()
                s.sendto(struct.pack('!cd', 'x', count), addr)  # !-network order, c-char, d-double
                # print "receive and sent: ",count
        except:
            traceback.print_exc()
        pass

    def send_work(self, session, interval, num):
        def inside(s, interval, num):
            tail = '.' * 100
            for i in range(0, num):
                paylaod = struct.pack('!cd', 'o', time.time()) + tail
                s.sendall(paylaod)
                time.sleep(interval)

        try:
            self.total_sent_time = timer(inside, session, interval, num)
        finally:
            session.sendall('')  # 通知server断开链接
            session.sendall('')

    def client_delay(self, host, port, num, verbose=True):
        # 向server发包，计算回包延时
        interval = 0.015  # ms
        diff = []
        total_delay = 0
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((host, port))
            thread.start_new_thread(self.send_work, (s, interval, num))

            count = None
            while True:
                data, addr = s.recvfrom(1024)
                t1 = time.time()
                c, count = struct.unpack('!cd', data[0:9])
                if c == 'x':
                    break
                diff.append(t1 - count)

            for d in diff:
                total_delay += d
            avg = total_delay * 1000.0 / len(diff)
            speed = num * 151 / self.total_sent_time / 1024
            loss = (num - len(diff)) * 100.0 / num
            if verbose:
                print '================================='
                print 'total_delay        : %.2fs' % total_delay
                print 'sent package num   : %d' % num
                print 'server received pkt: %d' % int(count)
                print 'client received pkt: %d' % len(diff)
                print 'lost               : %.2f%%' % loss
                print 'sent speed         : %.2fKB(%.2fKb)' % (speed, speed * 8)
                print 'sent interval      : %.2fms' % (interval * 1000)
                print 'avg delay          : %.2fms' % avg
                print '=================================\n'

            return loss, avg, speed
        except:
            traceback.print_exc()

    def main(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "csn:p:h:", [])

            for opt, arg in opts:
                if opt in ("-s",):
                    self.is_server = True
                elif opt in ("-c",):
                    self.is_server = False
                elif opt in ("-p",):
                    self.port = int(arg)
                elif opt in ("-h",):
                    self.host = arg
                elif opt in ("-n",):
                    self.num = int(arg)
                else:
                    usage()
                    sys.exit(-1)

            if self.is_server:
                if self.port <= 0:
                    usage('port cannot be NULL for server.')
                    sys.exit(-1)

                print "work as server, listen on port: ", str(self.port)
                self.server_delay(self.port)

            else:
                if self.port <= 0 or self.host == '':
                    usage('port and host cannot be NULL for client.')
                    sys.exit(-1)

                print "work as server, connect to host: ", self.host, ", port: ", str(self.port)
                self.client_delay(self.host, self.port, self.num)

        except Exception, e:
            print(e)
        pass


if __name__ == '__main__':
    delay = Delay()
    delay.main()
