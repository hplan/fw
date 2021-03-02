#!/usr/bin/env python

import os
from model import DatabaseExecutor as db
from setup import product_setup
from setup import bz_setup
import signal

executor = db.DatabaseExecutor()


def run():
    print """
    Release tool setup
    1.setup bugzilla profile
    2.setup product
    3.exit setup
    """
    while True:
        combo = raw_input("* What do you want to do: ")
        if not combo.isdigit():
            print "Unknown combo {0}\n".format(combo)
        elif int(combo) == 3:
            exit(0)
        elif int(combo) == 1:
            bz_setup.run()
        elif int(combo) == 2:
            product_setup.run()
            pass
        else:
            print "Unknown combo {0}\n".format(combo)


def on_signal_interrupt(signal, frame):
    print "\n\n bye ~"
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_signal_interrupt)

    if not os.path.exists("./db/fw.db"):
        executor.create_db()
    run()
