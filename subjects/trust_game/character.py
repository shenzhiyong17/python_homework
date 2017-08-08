#!/usr/bin/python
# -*- coding:utf-8 -*-
# 2017.08.07

from Game import Rule
import random


class Character:
    id = 0

    def __init__(self):
        self.money = Rule.base_fund
        self.rival_records = []
        self.rival_chose = True  # 上一轮对方选择
        self.self_chose = True  # 上一轮自己选择
        self.card = None
        Character.id += 1
        self.id = Character.id

    def __str__(self):
        return '%2s %s: %s' % (self.id, self.__class__, self.money)

    def __cmp__(self, other):
        if self.money < other.money:
            return -1
        elif self.money > other.money:
            return 1
        else:
            return 0

    def reset(self):
        self.rival_records = []
        self.rival_chose = True
        self.self_chose = True
        self.card = None

    def play(self):
        raise NotImplementedError

    def earn(self, rival_card, self_card):
        self.card = self_card
        if self.card:
            self.money -= Rule.ticket
        if rival_card and self.card:
            self.money += Rule.trust_win
            self.rival_chose = True
            self.self_chose = True
        elif not self.card and rival_card:
            self.money += Rule.cheat_win
            self.rival_chose = True
            self.self_chose = False
        elif not rival_card and self.card:
            self.rival_chose = False
            self.self_chose = True
        elif not rival_card and not self.card:
            self.rival_chose = False
            self.self_chose = False
        self.rival_records.append(rival_card)


class SimpleGirl(Character):
    # 傻白甜
    def play(self):
        return True


class Cheater(Character):
    # 老骗子
    def play(self):
        return False


class Repeater(Character):
    # 复读机，你上次怎样对我，我这次就怎样对你
    def play(self):
        return self.rival_chose


class BigMan(Character):
    # 黑社会，骗我一次就再也不相信你
    def play(self):
        if self.self_chose is False or self.rival_chose is False:
            return False
        else:
            return True


class MrTry(Character):
    # 合作合作欺骗合作，试探你的反应，如果你反击，我就变成复读机，如果你不反击，我就变成老骗子
    def __init__(self):
        Character.__init__(self)
        self.cards = [True, True, False, True]

    def reset(self):
        Character.reset(self)
        self.cards = [True, True, False, True]

    def play(self):
        if self.cards:
            return self.cards.pop(0)
        else:
            if False in self.rival_records:
                return self.rival_chose
            else:
                return False


class SmartRepeater(Character):
    # 包容的复读机。连续两次被欺骗才会选择欺骗
    def play(self):
        if len(self.rival_records) >= 2 and \
                        self.rival_records[-2] is False and self.rival_records[-1] is False:
            return False
        return True


class MrKeeper(Character):
    # 一根筋。我先合作，如果你也合作，我会选择跟上次一样，如果你欺骗，我会选择跟上次相反
    def play(self):
        if self.rival_chose:
            return self.self_chose
        else:
            return not self.self_chose


class MrRand(Character):
    # 胡乱来。随高兴胡乱选。
    def play(self):
        return random.choice([True, False])
