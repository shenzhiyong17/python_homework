#!/usr/bin/python
# -*- coding:utf-8 -*-
# https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328251266d86585fc9514536a638f06b41908d44000

import hashlib


def calc_md5(passwd):
    md5 = hashlib.md5()
    md5.update(passwd)
    return md5.hexdigest()


class PassDB:
    simple_db = {}
    db = {}
    salt = 'the-Salt'

    def gen_db(self, start_year=1980, end_year=2001):
        # 简单生日密码对照表
        years = ['%4d' % x for x in range(start_year, end_year)]
        months = ['%02d' % x for x in range(1, 13)]
        days = ['%02d' % x for x in range(1, 32)]
        birthdays = ['%s%s%s' % (year, month, day) for year in years for month in months for day in days]
        for birthday in birthdays:
            self.simple_db[calc_md5(birthday)] = birthday
        return self.simple_db

    def register(self, username, passwd):
        self.db[username] = calc_md5('%s%s%s' % (username, self.salt, passwd))

    def login(self, username, passwd):
        return self.db.get(username) == calc_md5('%s%s%s' % (username, self.salt, passwd))


if __name__ == '__main__':
    db = PassDB()
    db.register('shenzhiyong', '19840528')
    print db.login('shenzhiyong', '19840527')
    print db.login('shenzhiyong', '19840528')
