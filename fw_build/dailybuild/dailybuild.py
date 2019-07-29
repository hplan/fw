#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import getopt
import sys
import ConfigParser

if __name__ == '__main__':
    # getopt.getopt()
    parser = ConfigParser.ConfigParser()
    parser.read("./dailybuild.ini")
    # print sys.argv
    print "sleep 10"
    # print "make update-api\n"
    # print parser.get("eagle", "kernel_build_cmd")