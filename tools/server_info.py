import commands
import re
import time


class OutputFormat:
    def __init__(self):
        self.data = ''
        self.db = {}
        self.struct = {}

    def addtest(self, case_name, keys):
        self.db[case_name] = []
        self.struct[case_name] = keys

    def insert(self, case_name, values):
        self.db[case_name].append(values)

    def gen_report(self, span=16):
        span = "%" + "%ss" % span
        for testname in self.db.keys():
            self.data = self.data + testname + ' :\n'
            for j in self.struct[testname]:
                self.data += span % j
            self.data += '\n'
            for i in range(len(self.db[testname])):
                for j in self.struct[testname]:
                    test_data = span % (self.db[testname][i][j])
                    self.data += test_data
                self.data += '\n'
            self.data += '\n'
        return self.data

    def logout_report(self, logfile):
        if self.data != '':
            log = open(logfile, 'a')
            res = self.data + '\n'
            log.write(res)


def analysis_status():
    out = commands.getoutput('god status')

    result = {}
    pids = ''
    excption = ''
    pattern = '.*\\x1b\[[\d;]+m(.*)\\x1b\[\d+m\[(.*) .*\]:\s*\x1b\[[\d;]+m(.*)\\x1b\[\d+m(\s*\(.*\))?'
    for line in out.split('\n'):
        service, pid, status, start_time = re.match(pattern=pattern, string=line).groups()
        service = '_'.join(service.split('_')[-2:])
        if pid:
            result[pid] = {'service': service, 'pid': pid, 'status': status, 'start_time': start_time}
            pids += '%s,' % pid
        else:
            excption += line
            excption += '\n'
    pids = pids.rstrip(',')
    out = commands.getoutput('top -b -n 1 -p %s' % pids)
    load_average = re.match(pattern='.*load average: (.*)', string=out.split('\n')[0]).group(1)
    cpu_idle = re.match(pattern='.*, (\d*.\d*)[% ]id,.*', string=out.split('\n')[2]).group(1)
    for line in out.split('\n')[7:]:
        if line:
            pid, _user, _pr, _ni, _virt, _res, _shr, _s, cpu_percent, mem_percent, _time, _command = line.split()
            result[pid]['res'] = _res
            result[pid]['cpu_percent'] = cpu_percent
            result[pid]['mem_percent'] = mem_percent
    return result, cpu_idle, load_average


def pr_status(status):
    result, cpu_idle, load_average = status
    t = OutputFormat()
    t.addtest('service info', ['service', 'status', 'cpu_percent', 'mem_percent', 'res'])
    for pid in result:
        t.insert('service info', result[pid])

    print 'host: %s' % commands.getoutput('hostname')
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print 'cpu idle: %s' % cpu_idle
    print 'load average: %s' % load_average
    print t.gen_report(span=25)


if __name__ == '__main__':
    pr_status(analysis_status())
