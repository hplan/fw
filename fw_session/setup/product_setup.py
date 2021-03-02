#!/usr/bin/env python

import sys
sys.path.append("./model")
from model import DatabaseExecutor as db
from model import Product

executor = db.DatabaseExecutor()


def new_product():
    print "\n>> New product:\n"
    # print host
    name = raw_input("   Product name: ")
    # print name
    alias = raw_input("   Product alias: ")
    # print pwd
    pdir = raw_input("   Product dir: ")

    pd = Product.Product()
    pd.set("name", name)
    pd.set("alias", alias)
    pd.set("dir", pdir)
    executor.prod_add(pd)
    print "\n   Product created."


def edit_product(pds):
    print "\n>> Products:"
    print "   " + "-" * 60
    for pd in pds:
        print "     id:    |", pd['id']
        print "     name:  |", pd['name']
        print "     alias: |", pd['alias']
        print "     dir:   |", pd['dir']
        print "   " + "-" * 60

    # get user input
    while True:
        rid = raw_input("   * Choose product id: ")
        if not rid.isdigit():
            print "     Unknown combo {0}\n".format(rid)
        else:
            break
    print """
      >> Operations:\n
         1.Update name
         2.Update alias
         3.Update dir
         4.Exit
"""
    while True:
        combo = raw_input("         * What do you want to do: ")
        if not combo.isdigit():
            print "           Unknown combo {0}\n".format(combo)
        elif int(combo) == 1:
            name = raw_input("           Product name: ")
            pd = Product.Product()
            pd.set("name", name)
            prod_update(pd, rid)
        elif int(combo) == 2:
            alias = raw_input("           Product alias: ")
            pd = Product.Product()
            pd.set("alias", alias)
            prod_update(pd, rid)
        elif int(combo) == 3:
            pdir = raw_input("           Product dir: ")
            pd = Product.Product()
            pd.set("dir", pdir)
            prod_update(pd, rid)
        elif int(combo) == 4:
            exit(0)
        else:
            print "           Unknown combo {0}\n".format(combo)


def prod_update(pd, rid):
    executor.prod_update(pd, int(rid))
    print "           product updated.\n"


def product_setup():
    print "\n>> Operations:"
    products = executor.prod_query()
    if not products:
        new_product()
    else:
        print """
   1.Add product
   2.Update product
   3.Exit
"""
        while True:
            combo = raw_input("* What do you want to do: ")
            if not combo.isdigit():
                print "Unknown combo {0}\n".format(combo)
            elif int(combo) == 1:
                new_product()
                print ""
            elif int(combo) == 2:
                edit_product(products)
            elif int(combo) == 3:
                exit(0)
            else:
                print "Unknown combo {0}\n".format(combo)


def run():
    product_setup()
