#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import calendar
import os

FW_PREFIX = "21"


def get_months(n):
    date = datetime.datetime.today()
    month = date.month
    year = date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1)


def gs_months(fmt):
    fws = []
    print "ls | grep " + FW_PREFIX + fmt
    with os.popen("ls | grep " + FW_PREFIX + fmt) as b:
        for fwv in b.readlines():
            fws.append(fwv.replace("\n", ""))

    if fws.__len__() != 0:
        # remove the last item in queue
        fws.pop()
        # remove the first item in queue
        fws.__delitem__(0)
        mid = fws.__len__() / 2
        # remove the middle item in queue
        fws.__delitem__(mid)
        # keep 1, 15, 30
        # keep 1, 16, 31

    for fwv in fws:
        # os.system("rm -rf " + fwv)
        print "rm -rf ", fwv


if __name__ == '__main__':
    today = datetime.datetime.today()
    for i in range(12):
        today = get_months(i + 4)
        weekday, days = calendar.monthrange(today.year, today.month)
        fmt_ym = today.strftime(".%y.%m.")
        gs_months(fmt_ym)

