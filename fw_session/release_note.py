#!/usr/bin/env python
# -*- coding: utf-8 -*-
import BugzillaApi
import ConfigParser
import model.DatabaseExecutor as model
import model.git_utils as git_utils
import signal

executor = model.DatabaseExecutor()
controller = BugzillaApi.BugzillaApi()


def save_product(rid):
    config = ConfigParser.ConfigParser()
    config.add_section("product_section")
    config.set("product_section", "product_id", rid)
    config.write(open('.product.ini', "w"))


def run():
    # check bugzilla profile
    bz = executor.bz_query()
    prods = executor.prod_query()
    if not bz or not prods:
        print "Please continue after your personal information is perfected. "
        exit(0)

    print "*" * 50
    for pd in prods:
        print "%1s %-10s: %-34s %s" % ("*", "id", pd['id'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "name", pd['name'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "alias", pd['alias'], "*")
        print "%1s %-10s: %-34s %s" % ("*", "dir", pd['dir'], "*")
        print "%1s %-46s %s" % ("*", " ", "*")

    while True:
        rid = raw_input("%1s %-20s" % ("*", "choose product id: "))
        if not rid.isdigit():
            print "%1s %-46s %s" % ("*", "product id must be a number, unknown id: %s" % rid, "*")
        else:
            save_product(rid)
            break

    tag = raw_input("%1s %-20s" % ("*", "input compare tag: "))
    git_log_dir = git_utils.get_git_logs(tag)
    print " "
    print " git logs since %s:" % tag
    bugs = git_utils.parse_git_logs(git_log_dir)
    controller.get_bugs_info(bugs)
    print " "
    print " RESOLVED FIXED bugs on Bugzilla: "
    bug_ids = controller.get_release_note()

    # add comment support
    # ask for comment intent
    print " "
    post = raw_input("%1s %-20s" % ("*", "do you want to comment on these bug? (Y/N) "))
    if post == 'Y' or post == 'y':
        pass
    else:
        exit(0)

    # get input comment
    comment = raw_input("%1s %-20s" % ("*", "input the comment: \n"))
    print " "
    print "* your comment is: \n %s" % comment

    # secondary confirm
    print " "
    post = raw_input("%1s %-20s" % ("*", "Are you sure to comment on these bug? (Y/N) "))
    if post == 'Y' or post == 'y':
        pass
    else:
        exit(0)

    # do comment request
    for bug_id in bug_ids:
        controller.comment(bug_id, comment)


def on_signal_interrupt(signal, frame):
    print "\n\n bye~"
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, on_signal_interrupt)
    run()
