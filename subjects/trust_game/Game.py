#!/usr/bin/python
# -*- coding:utf-8 -*-
# 2017.08.07
# 信任的进化
from character import *
import tools.output_format as Format
import random
import dataStructure.common.gen_rand as gen_rand


class Rule:
    ticket = 1  # 投入
    trust_win = 2  # 共赢
    cheat_win = 3  # 作弊赢
    base_fund = 0  # 原始资本


class Trade:
    def __init__(self, gamer1, gamer2, count=20):
        self.gamer1 = gamer1
        self.gamer1.reset()
        self.gamer2 = gamer2
        self.gamer2.reset()
        self.count = count

    def play(self, mistake=0):
        for c in range(self.count):
            self.gamer1.card, self.gamer2.card = self.gamer1.play(), self.gamer2.play()
            if random.randint(0, 100) < mistake:
                self.gamer1.card = False
            if random.randint(0, 100) < mistake:
                self.gamer2.card = False
            self.gamer1.earn(self.gamer2.card, self.gamer1.card)
            self.gamer2.earn(self.gamer1.card, self.gamer2.card)


class Game:
    def __init__(self, number=20, kick_off=5, characters=None, gamers=None, max_round=10, trade=10, mistake=0):
        if not gamers:
            self.characters = characters
            gamers = []
            self.number = number
            for i in range(number):
                gamer = self.characters[i % len(self.characters)]()
                gamers.append(gamer)
        else:
            self.characters = set()
            for g in gamers:
                self.characters.add(g.__class__)
        self.kick_off = kick_off
        self.gamers = gamers
        self.max_round = max_round
        self.trade = trade
        self.mistake = mistake
        self.output = Format.output_format()
        title = []
        for c in self.characters:
            title.append(c)
        self.output.addtest('change', title)
        print '--- init done ---'

    def start(self, verbose=False):
        for i in self.gamers:
            i.money = Rule.base_fund
        for i in range(0, len(self.gamers) - 1):
            for j in range(i + 1, len(self.gamers)):
                pair = self.gamers[i], self.gamers[j]
                if verbose:
                    for g in pair:
                        print g
                trade = Trade(count=self.trade, *pair)
                trade.play(mistake=self.mistake)
                if verbose:
                    for g in pair:
                        print g
                    print '**************'
        self.gamers.sort()
        # for g in self.gamers:
        #     print g
        # print '-----------------------'
        self.gamers = self.gamers[self.kick_off:]
        for i in self.gamers[-self.kick_off:]:
            self.gamers.append(i.__class__())

    def end(self):
        cls = self.gamers[0].__class__
        for i in self.gamers[1:]:
            if i.__class__ != cls:
                return False
        return True

    def run_to_end(self, verbose=False):
        rnd = 0
        while not self.end() and rnd < self.max_round:
            self.start(verbose)
            self.count()
            rnd += 1
        print self.output.gen_report(span=26)

    def count(self):
        item = {}
        for c in self.characters:
            n = 0
            for p in self.gamers:
                if isinstance(p, c):
                    n += 1
            item[c] = n if n else ''
        self.output.insert('change', item)


if __name__ == '__main__':
    characters = [
        SimpleGirl,
        Cheater,
        BigMan,
        Repeater,
        SmartRepeater,
        MrTry,
        MrKeeper,
        MrRand,
    ]
    gamers = []
    gamers += [Cheater() for i in range(20)]
    gamers += [Repeater() for i in range(5)]
    gamers += [SmartRepeater() for i in range(5)]
    gamers += [MrKeeper() for i in range(5)]
    gamers += [MrTry() for i in range(5)]
    gamers += [MrRand() for i in range(5)]
    gamers += [BigMan() for i in range(5)]
    # gamers += [SimpleGirl() for i in range(10)]
    gen_rand.disorder(gamers)
    game = Game(number=40, kick_off=5, gamers=gamers, characters=characters, max_round=20, trade=40, mistake=5)
    game.run_to_end(verbose=False)

    # a = SimpleGirl()
    # b = BigMan()
    # pk = PK(a, b, 1)
    # pk.play()
