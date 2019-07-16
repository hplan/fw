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

    rid = raw_input("%1s %-20s" % ("*", "choose product id: "))
    save_product(rid)

    tag = raw_input("%1s %-20s" % ("*", "input compare tag: "))
    git_log_dir = git_utils.get_git_logs(tag)
    print "\ngit logs since " + tag + ":\n"
    bugs = git_utils.parse_git_logs(git_log_dir)
    # bugs = [140237, 140240, 140241]
    controller.get_bugs_info(bugs)


if __name__ == "__main__":
    run()
