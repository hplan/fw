#!/usr/bin/env python

import getpass
import sys
sys.path.append("./model")

from model import DatabaseExecutor as db
from model import Bz

executor = db.DatabaseExecutor()


def new_profile():
    # print host
    host = raw_input("%1s %-14s" % ("*", "bugzilla host: "))
    # print name
    name = raw_input("%1s %-14s" % ("*", "bugzilla name: "))
    # print pwd
    pwd = getpass.getpass("%1s %-14s" % ("*", "bugzilla password: "))

    bz = Bz.Bz()
    bz.set("bz_name", name)
    bz.set("bz_host", host)
    bz.set("bz_pwd", pwd)
    executor.bz_add(bz)
    print "%1s %-46s %s" % ("*", " ", "*")
    print "%1s %-46s %s" % ("*", "profile created.", "*")


def edit_profile(bz):
    print "%1s %-14s %-31s %s" % ("*", "bugzilla host:", bz.get("bz_host"), "*")
    print "%1s %-14s %-31s %s" % ("*", "bugzilla name:", bz.get("bz_name"), "*")
    print "%1s %-14s %-27s %s" % ("*", "bugzilla password:", "******", "*")
    print "%1s %-46s %s" % ("*", " ", "*")
    print "%1s %-46s %s" % ("*", "1. update host", "*")
    print "%1s %-46s %s" % ("*", "2. update name", "*")
    print "%1s %-46s %s" % ("*", "3. update password", "*")
    print "%1s %-46s %s" % ("*", "4. show password", "*")
    print "%1s %-46s %s" % ("*", "5. clear token", "*")
    print "%1s %-46s %s" % ("*", "6. exit", "*")

    while True:
        # get user input
        print "%1s %-46s %s" % ("*", " ", "*")
        combo = raw_input("%1s %-25s" % ("*", "what do you want to do: "))
        if not combo.isdigit():
            print "%1s %-46s %s" % ("*", " %s is not a number" % combo, "*")
        elif int(combo) == 1:
            host = raw_input("%1s %-13s" % ("*", "update host: "))
            bz = Bz.Bz()
            bz.set("bz_host", host)
            bz_update(bz)
        elif int(combo) == 2:
            name = raw_input("%1s %-13s" % ("*", "update name: "))
            bz = Bz.Bz()
            bz.set("bz_name", name)
            bz_update(bz)
        elif int(combo) == 3:
            pwd = getpass.getpass("%1s %-17s" % ("*", "update password: "))
            bz = Bz.Bz()
            bz.set("bz_pwd", pwd)
            bz_update(bz)
        elif int(combo) == 4:
            bz = executor.bz_query()
            print "%1s %-46s %s" % ("*", "password: %s" % bz['bz_pwd'], "*")
        elif int(combo) == 5:
            bz = Bz.Bz()
            bz.set("bz_token", "")
            executor.bz_update(bz)
        elif int(combo) == 6:
            print ("*" * 50)
            exit(0)
        else:
            print "%1s %-46s %s" % ("*", "unknown combo %s" % combo, "*")


def bz_update(bz):
    executor.bz_update(bz)
    print "%1s %-46s %s" % ("*", "profile updated.", "*")


def profile_setup():
    print "%1s %-46s %s" % ("*", " ", "*")
    bz = executor.bz_query()
    if not bz:
        print "%1s %-46s %s" % ("*", "did not find profile", "*")
        print "%1s %-46s %s" % ("*", " ", "*")
        new_profile()
    else:
        print "%1s %-46s %s" % ("*", "profile exists", "*")
        print "%1s %-46s %s" % ("*", " ", "*")
        edit_profile(bz)


def run():
    profile_setup()
