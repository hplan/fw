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

    print "\nRelease tools\n"
    print "  All git logs will saved in fw/fw_session/git-logs.txt"
    print "  All resolved bugs will saved in fw/fw_session/resolved_bugs.txt"
    print ""
    print ">> Products:"
    for pd in prods:
        print "   --------------------------------------------------------"
        print "     id:    |", pd['id']
        print "     name:  |", pd['name']
        print "     alias: |", pd['alias']
        print "     dir:   |", pd['dir']
    print "   --------------------------------------------------------"

    while True:
        rid = raw_input("* Choose product id: ")
        if not rid.isdigit():
            print "Unknown combo {0}\n".format(rid)
        else:
            save_product(rid)
            break

    tag = raw_input("* Input the compare tag: ")
    git_log_dir = git_utils.get_git_logs(tag)
    print " "
    print ">> Git commit:"
    print "   >> Git logs since %s:" % tag
    bugs = git_utils.parse_git_logs(git_log_dir)
    controller.get_bugs_info(bugs)
    print " "
    print ">> Bugzilla:"
    print "   >> RESOLVED FIXED bugs:"
    bug_ids = controller.get_release_note()

    # add comment support
    # ask for comment intent
    print " "
    post = raw_input("* Do you want to comment on these bug? (Y/N) ")
    if post == 'Y' or post == 'y':
        pass
    else:
        exit(0)

    # get input comment
    comment = raw_input("* Input the comment: \n")
    print " "
    print "* your comment is: \n %s" % comment

    # secondary confirm
    print " "
    post = raw_input("* Are you sure to comment on these bug? (Y/N) ")
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
