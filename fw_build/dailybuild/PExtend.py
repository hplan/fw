#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 50600 - 51500, the same as 4xx, 17xx, 18xx but for Accounts 7 to 16
# 51600 - 52500, the same as 2300 - 2899 but for Accounts 7 to 16
# 52600 - 53500, the same as 26001 - 26599 but for Accounts 7 to 16
# 53600 - 54500, the same as 29001 –  but for Accounts 7 to 16

import sys


def guess_possible_range(pVal):
    if pVal < 400:
        print "Sorry, i don't know."
        sys.exit(1)

    decade = pVal % 100
    if 400 < pVal < 700 or 1700 < pVal < 1900:
        print "Sorry, i don't know about account 1."
        test(decade, 400, 700)
        test(decade, 1700, 1801)
        test(decade, 50600, 51501)
    elif 2300 < pVal < 2900:
        test(decade, 2300, 2900)
        test(decade, 51600, 52501)
    elif 26000 < pVal < 26600:
        test(decade, 26000, 26600)
        test(decade, 52600, 53501)
    elif 29000 < pVal:
        test(decade, 29000, 29559)
        test(decade, 53600, 54501)


def test(decade, lt, ht, step=100):
    for i in range(lt, ht, step):
        print i + decade


def run():
    pVal = raw_input("input pvalue: ")
    if not pVal.isdigit():
        print "invalid argument"
        sys.exit(1)

    guess_possible_range(int(pVal))


if __name__ == '__main__':
    run()
