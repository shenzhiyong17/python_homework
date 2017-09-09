#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telnetlib
import time
import re


def telnet_cmd(Host, username, password, cmd, timeout=15, verbose=False, background=False):
    finish = ':~# '
    tn = None
    res = ''
    cmds = cmd.strip('\n').split('\n')

    try:
        tn = telnetlib.Telnet(Host)
        tn.read_until('login:')
        tn.write(username + '\n')

        tn.read_until('Password:')
        tn.write(password + '\n')

        tn.read_until(finish)
        for cmd in cmds:
            # print 'cmd: ',cmd
            if background:
                tn.write('nohup %s & \n' % cmd)
                time.sleep(1)
                return
            else:
                tn.write('%s\n' % cmd)
            res = tn.read_until(finish, timeout=timeout)
            cmd.encode('ascii')
            cmd = re.sub('\?', '\\?', cmd)
            cmd = re.sub('\.', '\\.', cmd)
            res = re.sub('%s[\r]?\r\n' % cmd, '', res)
            res = re.sub('[\r]\n[^\n]*%s$' % finish, '', res)
            if verbose:
                print res
    except Exception, ex:
        print str(ex)
    finally:
        if tn is not None:
            tn.close()
    return res


if __name__ == "__main__":
    cmd = 'curl http://localhost/cgi-bin/luci/service/internal/ipv6?cmd=3'
    # cmd = 'uci -q get network.wan.ifname'
    tn = lambda command: telnet_cmd(Host='192.168.31.1', username='root', password='admin', cmd=command, background=False)
    print tn(cmd)
    # print telnet_cmd('192.168.31.1', 'root', 'admin', cmd, 5, background=False)
