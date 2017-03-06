#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-1-18

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError