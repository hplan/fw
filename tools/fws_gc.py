#!/usr/bin/env python
import os

import datetime


FW_PREFIX = "54"


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
        os.system("rm -rf " + fwv)
        print "rm -rf ", fwv


def gc_last_year(year):
    fw_name = FW_PREFIX + ".%d.*" % (year % 2000)
    print "rm -rf " + fw_name
    os.system("rm -rf " + fw_name)


if __name__ == '__main__':
    # delete last year fws
    now = datetime.datetime.now()
    gc_last_year(now.year - 1)

    # delete previous months fws
    today = datetime.datetime.today()
    today = today.replace(month=today.month - 2)
    yms = range(1, now.month - 2)
    for month in yms:
        today = today.replace(month=today.month - 1)
        fmt_ym = today.strftime('.%y.%m.')
        gs_months(fmt_ym)
