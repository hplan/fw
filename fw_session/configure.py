#!/usr/bin/env python

import os
from model import DatabaseExecutor as db
from setup import product_setup
from setup import bz_setup

executor = db.DatabaseExecutor()


def run():
    print """
    Tools setup process
        1. setup bugzilla profile configuration
        2. setup product configuration
        3. exit
    """
    while True:
        print ("*" * 50)
        combo = raw_input("%1s %-25s" % ("*", "what do you want to do: "))
        if not combo.isdigit():
            print "%1s %-46s %s" % ("*", " %s is not a number" % combo, "*")
        elif int(combo) == 3:
            print ("*" * 50)
            exit(0)
        elif int(combo) == 1:
            bz_setup.run()
        elif int(combo) == 2:
            product_setup.run()
            pass
        else:
            print "%1s %-46s %s" % ("*", "unknown combo %s" % combo, "*")


if __name__ == '__main__':
    if not os.path.exists("./db/fw.db"):
        print "not exists"
        executor.create_db()
    run()
