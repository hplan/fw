#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import collections
import smtplib
from email.mime.text import MIMEText

PER_THRESHOLD = 95                  # more than 95% used
AVL_THRESHOLD = 10 * 1024 * 1024    # available less than 10GB
SVR_LIST = ['192.168.120.166', '192.168.120.239', '192.168.120.32', '192.168.120.33']
MAIL_TO = "hplan@grandstream.cn,gwzhang@grandstream.cn,bxpan@grandstream.cn,xlli@grandstream.cn,ahluo@grandstream.cn," \
          "jcai@grandstream.cn"
TMP_FILE = "/tmp/snmpdf.html"
message = ""


def snmp_walk(host, oid):
    result = os.popen('snmpwalk -v 2c -c hplan ' + host + ' ' + oid).read().split("\n")[:-1]
    return result


# 测试用
def snmp_walk_raw(host, oid):
    result = os.popen('snmpwalk -v 2c -c hplan ' + host + ' ' + oid).read()
    return result


def parse_storage_desc(data, oid):
    if data:
        respond = collections.OrderedDict()
        for d in data:
            d = d.replace(" ", "").replace("HOST-RESOURCES-MIB::", "").split("=")
            index = d[0][len(oid) + 1:]
            name = d[1].replace("STRING:", "")
            if name.startswith("/"):
                respond[index] = name
        return respond
    else:
        pass


def parse_int(data, oid):
    if data:
        respond = collections.OrderedDict()
        for d in data:
            d = d.replace(" ", "").replace("HOST-RESOURCES-MIB::", "").split("=")
            index = d[0][len(oid) + 1:]
            v = int(d[1].replace("INTEGER:", "").replace("Bytes", ""))
            respond[index] = v
        return respond
    else:
        pass


def send_mail(username, passwd, recv, title, content, mail_host='smtp.qiye.163.com', port=25):
    """
    发送邮件函数，默认使用163smtp
    :param username: 邮箱账号 xx@163.com
    :param passwd: 邮箱密码
    :param recv: 邮箱接收人地址，多个账号以逗号隔开
    :param title: 邮件标题
    :param content: 邮件内容
    :param mail_host: 邮箱服务器
    :param port: 端口号
    :return:
    """

    msg = MIMEText(content, 'html', 'utf-8')  # 邮件内容
    msg['Subject'] = title  # 邮件主题
    msg['From'] = username  # 发送者账号
    msg['To'] = recv  # 接收者账号列表
    smtp = smtplib.SMTP(mail_host, port=port)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
    smtp.login(username, passwd)  # 发送者的邮箱账号，密码
    smtp.sendmail(username, recv.split(","), msg.as_string())
    # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
    print('email send success.')


def get_human_reading_size(size):
    a = round(1.0 * size / 1024 / 1024, 2)
    if a > 2048:
        return str(round(1.0 * a / 1024, 2)) + "G"
    else:
        return str(a) + "M"


def print_sys(dev_desc, dev_size, dev_used, cb):
    column = ["Mount on", "Total", "Used", "Avail", "Percent"]

    f.writelines("<pre>%-30s%-10s%-10s%-10s%-10s</pre>" % tuple(column))

    for k, v in dev_desc.iteritems():
        total = dev_size.get(k)
        used = dev_used.get(k)
        if not total:
            total = 0
        if not used:
            used = 0

        avail = total - used
        if used == 0 and total == 0:
            used_per = 0
        else:
            used_per = round((1.0 * used / total) * 100, 2)

        fmt_val = (v, get_human_reading_size(total), get_human_reading_size(used), get_human_reading_size(avail),
                   str(used_per) + "%")

        print "%-30s%-10s%-10s%-10s%-10s" % fmt_val
        if used_per > PER_THRESHOLD and avail < AVL_THRESHOLD:
            cb["warning"] = True
            f.writelines("<pre style='color:Red;font-weight:bold;'>%-30s%-10s%-10s%-10s%-10s</pre>" % fmt_val)
        else:
            f.writelines("<pre>%-30s%-10s%-10s%-10s%-10s</pre>" % fmt_val)
    f.writelines("<br/><HR/>")


def walk_server(address, callback, f):
    if address:
        target = address
    else:
        target = "localhost"

    f.writelines("<h1>%s</h1>" % target)

    if sys.argv.__len__() != 1:
        target = sys.argv[1]

    #
    data = snmp_walk(target, "hrStorageDescr")
    dev_desc_resp = parse_storage_desc(data, "hrStorageDescr")

    # 簇的大小
    cluster_units = snmp_walk(target, "hrStorageAllocationUnits")
    cluster_units_resp = parse_int(cluster_units, "hrStorageAllocationUnits")

    # 簇的数目
    cluster_size = snmp_walk(target, "hrStorageSize")
    cluster_size_resp = parse_int(cluster_size, "hrStorageSize")

    # 使用多少, 跟总容量相除就是占用率
    used_data = snmp_walk(target, "hrStorageUsed")
    cluster_used_resp = parse_int(used_data, "hrStorageUsed")

    dev_size_resp = collections.OrderedDict()
    dev_used_resp = collections.OrderedDict()
    for k, v in cluster_units_resp.iteritems():
        if k in cluster_size_resp:
            dev_size_resp[k] = cluster_size_resp.get(k) * v
            dev_used_resp[k] = cluster_used_resp.get(k) * v
        else:
            continue

    print_sys(dev_desc_resp, dev_size_resp, dev_used_resp, callback)


if __name__ == '__main__':
    level = {"warning": False}

    with open(TMP_FILE, "w+") as f:
        f.writelines("<html><body>")
        for svr in SVR_LIST:
            walk_server(svr, level, f)
        f.writelines("</body></html>")
    f.close()

    if level["warning"]:
        email_user = 'hplan@grandstream.cn'
        email_pwd = 'Dev_1_3614'
        # TEST_MAIL_TO = "hplan@grandstream.cn"
        subject = 'Warning: No space left on build server.'
        with open(TMP_FILE, "r") as f:
            content = f.read()
        send_mail(email_user, email_pwd, MAIL_TO, subject, content)
