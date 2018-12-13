#!/usr/bin/python2.7

import time
import color_format


class output_format:
    def __init__(self):
        self.data = ''
        self.db = {}
        self.struct = {}

    def addtest(self,testname,keys):
        self.db[testname] = []
        self.struct[testname] = keys

    def insert(self,testname,values):
        self.db[testname].append(values)

    def gen_report(self,span=16):
        span = "%" + "%ss" % span
        for testname in self.db.keys():
            self.data = self.data + testname + ' :\n'
            for j in self.struct[testname]:
                self.data = self.data + span % j
            self.data = self.data + '\n'
            for i in range(len(self.db[testname])):
                for j in self.struct[testname]:
                    test_data = span % (self.db[testname][i][j])
                    if self.db[testname][i][j] == 'fail' or self.db[testname][i][j] is False:
                        test_data = color_format(test_data, fontcolor='red',mode='highlight')
                    # else:
                        # test_data = color_format(test_data)
                    self.data = self.data + test_data
                self.data = self.data + '\n'
            self.data = self.data + '\n'
        return self.data

    def logout_report(self,logfile):
        if self.data != '':
            log = open(logfile,'a')
            # res = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n' + self.data + '\n'
            res = self.data + '\n'
            log.write(res)
            # log.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            # log.write('\n')
            # log.write(self.data)
            # log.write('\n')


if __name__ == '__main__':
    item1 = {'upload':'10M','download':'20M','description':'lan','result':'pass'}
    item2 = {'upload':'30M','download':'40M','description':'2.4G','result':'fail'}
    item3 = {'upload':'30M','download':'40M','description':'2.4G','result':'pass'}
    item4 = {'upload':'30M','download':'40M','description':'2.4G','result':'fail'}
    t = output_format()
    t.addtest('qos',['description','upload','download','result'])
    t.addtest('test',['description','upload','download','result'])
    t.insert('test',item1)
    t.insert('test',item2)
    t.insert('qos',item3)
    t.insert('qos',item4)
    print t.gen_report(span=10)
