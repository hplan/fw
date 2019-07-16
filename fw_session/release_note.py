#!/usr/bin/env python
import BugzillaApi
import ConfigParser
import model.DatabaseExecutor as model
import model.git_utils as git_utils

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
    print "\ngit logs since " + tag + ":\n"
    bugs = git_utils.parse_git_logs(git_log_dir)
    controller.get_bugs_info(bugs)
    controller.get_release_note()

    # TODO: add comment support


if __name__ == "__main__":
    run()
