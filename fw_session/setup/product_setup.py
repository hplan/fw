#!/usr/bin/env python

import sys
sys.path.append("./model")
from model import DatabaseExecutor as db
from model import Product

executor = db.DatabaseExecutor()


def new_product():
    # print host
    name = raw_input("%1s %-14s" % ("*", "product name: "))
    # print name
    alias = raw_input("%1s %-14s" % ("*", "product alias: "))
    # print pwd
    pdir = raw_input("%1s %-14s" % ("*", "product dir: "))

    pd = Product.Product()
    pd.set("name", name)
    pd.set("alias", alias)
    pd.set("dir", pdir)
    executor.prod_add(pd)
    print "%1s %-46s %s" % ("*", " ", "*")
    print "%1s %-46s %s" % ("*", "product created.", "*")


def edit_product(pds):
    print "%1s %-46s %s" % ("*", " ", "*")
    for pd in pds:
        print "%1s %-10s: %-34s %s" % ("*", "id", pd['id'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "name", pd['name'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "alias", pd['alias'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "dir", pd['dir'], "*")
        print "%1s %-46s %s" % ("*", " ", "*")

    # get user input
    while True:
        print "%1s %-46s %s" % ("*", "-" * 46, "*")
        rid = raw_input("%1s %-20s" % ("*", "choose product id:"))
        if not rid.isdigit():
            print "%1s %-46s %s" % ("*", " %s is not a number" % rid, "*")
        else:
            break

    while True:
        print "%1s %-46s %s" % ("*", "-" * 46, "*")
        print "%1s %-46s %s" % ("*", " ", "*")
        print "%1s %-46s %s" % ("*", "1. update name", "*")
        print "%1s %-46s %s" % ("*", "2. update alias", "*")
        print "%1s %-46s %s" % ("*", "3. update dir", "*")
        print "%1s %-46s %s" % ("*", "4. exit", "*")
        print "%1s %-46s %s" % ("*", " ", "*")

        combo = raw_input("%1s %-25s" % ("*", "what do you want to do: "))
        if not combo.isdigit():
            print "%1s %-46s %s" % ("*", " %s is not a number" % combo, "*")
        elif int(combo) == 1:
            name = raw_input("%1s %-14s" % ("*", "product name: "))
            pd = Product.Product()
            pd.set("name", name)
            prod_update(pd, rid)
        elif int(combo) == 2:
            alias = raw_input("%1s %-14s" % ("*", "product alias: "))
            pd = Product.Product()
            pd.set("alias", alias)
            prod_update(pd, rid)
        elif int(combo) == 3:
            pdir = raw_input("%1s %-14s" % ("*", "product dir: "))
            pd = Product.Product()
            pd.set("dir", pdir)
            prod_update(pd, rid)
        elif int(combo) == 4:
            print ("*" * 50)
            exit(0)
        else:
            print "%1s %-46s %s" % ("*", "unknown combo %s" % combo, "*")


def prod_update(pd, rid):
    executor.prod_update(pd, int(rid))
    print "%1s %-46s %s" % ("*", "product updated.", "*")


def product_setup():
    print "%1s %-46s %s" % ("*", " ", "*")
    products = executor.prod_query()
    if not products:
        print "%1s %-46s %s" % ("*", "did not find product", "*")
        print "%1s %-46s %s" % ("*", " ", "*")
        new_product()
    else:
        print "%1s %-46s %s" % ("*", "1. add product", "*")
        print "%1s %-46s %s" % ("*", "2. update product", "*")
        print "%1s %-46s %s" % ("*", "3. exit", "*")
        print "%1s %-46s %s" % ("*", " ", "*")

        while True:
            print ("*" * 50)
            combo = raw_input("%1s %-25s" % ("*", "what do you want to do: "))
            if not combo.isdigit():
                print "%1s %-46s %s" % ("*", " %s is not a number" % combo, "*")
            elif int(combo) == 1:
                new_product()
            elif int(combo) == 2:
                edit_product(products)
            elif int(combo) == 3:
                print ("*" * 50)
                exit(0)
            else:
                print "%1s %-46s %s" % ("*", "unknown combo %s" % combo, "*")


def run():
    product_setup()
