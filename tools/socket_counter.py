#!/usr/sbin/env python


proc_files = ("/proc/net/netstat", "/proc/net/snmp")

def parse_proc_files(fn):
    stats = {}
    lines = file(fn).readlines()
    n_lines = len(lines)
    n = 0
    while n < n_lines:
        titles = lines[n].split(" ") # TcpExt: TcpXX SackXX
        values = lines[n+1].split(" ") # TcpExt: 11 23213
        kind = titles[0]
        del titles[0]
        del values[0]
        sub_stats = stats.get(kind, {})
        n_cols = len(titles)
        for i in range(n_cols):
            sub_stats[titles[i].strip()] = values[i].strip()
        stats[kind] = sub_stats
        n += 2
    return stats


def show_parsed(stats):
    kind_list = stats.keys()
    kind_list.sort()
    for kind in kind_list:
        title_list = stats[kind].keys()
        title_list.sort()
        for title in title_list:
            print "%-10s%-25s\t%20s" % (kind, title, stats[kind][title])

s = {}
for fn in proc_files:
    new_s = parse_proc_files(fn)
    for new_kind in new_s:
        if new_kind not in s: # unlikely
            s[new_kind] = new_s[new_kind]
        else:
            s[new_kind].update(new_s[new_kind])

show_parsed(s)