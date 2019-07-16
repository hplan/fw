#!/usr/bin/env python
import os
import re
import ConfigParser
import DatabaseExecutor as db
executor = db.DatabaseExecutor()

project_dir = None


def __load_config():
    config = ConfigParser.ConfigParser()
    config.readfp(open('./.product.ini'))
    product_id = config.getint("product_section", "product_id")
    product = executor.get_product(product_id)

    global project_dir
    project_dir = product.get_product_dir()


def get_git_logs(tag):
    if not project_dir:
        __load_config()

    t = os.getcwd() + '/git-logs.txt'
    os.system("cd " + str(project_dir)
              + " && repo forall -c 'git log --format=%s --no-merges ..." + tag + "' > "
              + t + " 2> /dev/null")
    return t


def parse_git_logs(fp):
    bugs = []
    with open(fp, 'r') as load_f:
        iterator = load_f.readlines()
        for line in iterator:
            if not line:
                continue
            summary = re.search('bug([\t ]*)(.*)\d+', line.lower())
            if summary:
                num_list = re.findall('\d+\.?\d*', summary.group())
                if num_list:
                    bugs.append(num_list[0])
    load_f.close()
    return bugs


