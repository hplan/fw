#!/usr/bin/env python
from model import DatabaseExecutor as db
from model import Bz
import getpass
import sys
sys.path.append("./model")
executor = db.DatabaseExecutor()


def new_profile():
    # print host
    print "   Bugzilla host: https://bugzilla.grandstream.com/bugzilla"
    host = "https://bugzilla.grandstream.com/bugzilla"
    # print name
    name = raw_input("   Bugzilla name: ")
    # print pwd
    pwd = getpass.getpass("   Bugzilla password: ")

    bz = Bz.Bz()
    bz.set("bz_name", name)
    bz.set("bz_host", host)
    bz.set("bz_pwd", pwd)
    executor.bz_add(bz)
    print "\n   Profile created."


def edit_profile(bz):
    host = bz.get("bz_host")
    print "   " + "-" * (len(host) + 25)
    print "     Bugzilla host:     |", bz.get("bz_host")
    print "     Bugzilla name:     |", bz.get("bz_name")
    print "     Bugzilla password: |", "******"
    print "   " + "-" * (len(host) + 23)
    print "\n>> Operations:"
    print """
   1.update host
   2.update name
   3.update password
   4.show password
   5.clear token
   6.exit
"""

    while True:
        # get user input
        combo = raw_input("* What do you want to do: ")
        if not combo.isdigit():
            print "Unknown combo {0}\n".format(combo)
        elif int(combo) == 1:
            host = raw_input("   new host: ")
            bz = Bz.Bz()
            bz.set("bz_host", host)
            bz_update(bz)
            print ""
        elif int(combo) == 2:
            name = raw_input("   new name: ")
            bz = Bz.Bz()
            bz.set("bz_name", name)
            bz_update(bz)
            print ""
        elif int(combo) == 3:
            pwd = getpass.getpass("   new password: ")
            bz = Bz.Bz()
            bz.set("bz_pwd", pwd)
            bz_update(bz)
            print ""
        elif int(combo) == 4:
            bz = executor.bz_query()
            print "   password: {0}\n".format(bz['bz_pwd'])
        elif int(combo) == 5:
            bz = Bz.Bz()
            bz.set("bz_token", "")
            executor.bz_update(bz)
            print "   Cleared.\n"
        elif int(combo) == 6:
            exit(0)
        else:
            print "Unknown combo {0}\n".format(combo)


def bz_update(bz):
    executor.bz_update(bz)
    print "   profile updated."


def profile_setup():
    print "\n>> Profile:"
    bz = executor.bz_query()
    if not bz:
        print ">> New profile:\n"
        new_profile()
        exit(0)
    else:
        print "   Profile already exists.\n"
        edit_profile(bz)


def run():
    profile_setup()
