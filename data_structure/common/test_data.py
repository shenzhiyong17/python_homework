#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2017-02-16

from data_structure.common import gen_rand

rand = gen_rand.gen_rand_list(15, 1, 100)


def rand_list(size):
    return gen_rand.gen_rand_list(size, 1, 100)
