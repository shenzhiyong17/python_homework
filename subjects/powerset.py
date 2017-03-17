#!/usr/bin/env python
# -*- coding: utf-8 -*-


def powerset(s, a=None):
    # 返回全部子元组
    if not a:
        a = s[0]
        s = s[1:]
    if not s:
        return (), (a,)
    else:
        r = ()
        for x in powerset(s[1:], s[0]):
            r = r + ((x + (a,)),)
        return powerset(s[1:], s[0]) + r


if __name__ == '__main__':
    s = ('a', 'b', 'c')
    print powerset(s)
