#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, random

# 1
a = list("Iphone7拍摄效果")
h = ''
l = ''
while a:
    s = a.pop(0)
    if s in string.letters:
        smy = 's'
    elif s in string.digits:
        smy = 'd'
    elif s == '\xe6':
        s += a.pop(0) + a.pop(0)
        smy = 'o'
    if l != smy or smy == 'o':
        s = ' ' + s
    h += s
    l = smy
print h.strip()
