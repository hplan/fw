#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import collections
import smtplib
from email.mime.text import MIMEText

THRESHOLD = 95
message = ""


def snmp_walk(host, oid):
    result = os.popen('snmpwalk -v 2c -c hplan ' + host + ' ' + oid).read().split("\n")[:-1]
    return result


def snmp_walk_raw(host, oid):
    result = os.popen('snmpwalk -v 2c -c hplan ' + host + ' ' + oid).read()
    return result


def parse_str(data, oid):
    if data:
        respond = collections.OrderedDict()
        for d in data:
            d = d.replace(" ", "").split("=")
            index = d[0][15 + len(oid):]
            name = d[1][7:]
            respond[index] = name
        return respond
    else:
        pass


def parse_int(data, oid):
    if data:
        respond = collections.OrderedDict()
        for d in data:
            d = d.replace(" ", "").split("=")
            index = d[0][15 + len(oid):]
            v = int(d[1][8:])
            respond[index] = v
        return respond
    else:
        pass


def print_sys(respond_list, callback):
    column = ["FileSystem", "Mount on",  "Total", "Used", "Avail", "Percent"]

    rev_map = collections.OrderedDict()
    for k in respond_list[0].keys():
        i = 0
        v = {}
        for col in column:
            v[col] = respond_list.__getitem__(i).get(k)
            i = i+1
        rev_map[k] = v

    with open("/tmp/snmpdf", "w+") as f:
        f.writelines("%-15s%-30s%-10s%-10s%-10s%-10s\n" % tuple(column))

        for k, v in rev_map.iteritems():
            if v[column.__getitem__(2)] == 0 or v[column.__getitem__(3)] == 0 \
                    or v[column.__getitem__(4)] == 0 or v[column.__getitem__(5)] == 0:
                continue

            total = v[column.__getitem__(2)]
            used = v[column.__getitem__(3)]
            avail = v[column.__getitem__(4)]
            percent = round((1 - (1.0 * avail / total)) * 100, 2)
            f.writelines("%-15s%-30s%-10s%-10s%-10s%-10s\n" % (
                v[column.__getitem__(0)],
                v[column.__getitem__(1)],
                str(round(1.0 * total / 1024 / 1024, 2)) + "G",
                str(round(1.0 * used / 1024 / 1024, 2)) + "G",
                str(round(1.0 * avail / 1024 / 1024, 2)) + "G",
                str(percent) + "%"))

            if percent > THRESHOLD:
                callback["warning"] = True
        f.close()


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

    msg = MIMEText(content)  # 邮件内容
    msg['Subject'] = title  # 邮件主题
    msg['From'] = username  # 发送者账号
    msg['To'] = recv  # 接收者账号列表
    smtp = smtplib.SMTP(mail_host, port=port)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
    smtp.login(username, passwd)  # 发送者的邮箱账号，密码
    smtp.sendmail(username, recv, msg.as_string())
    # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
    print('email send success.')


if __name__ == '__main__':
    devices = {}
    target = "localhost"
    cmd_list = ["dskDevice", "dskPath"]
    if sys.argv.__len__() != 1:
        target = sys.argv[1]

    respond_list = []
    for cmd in cmd_list:
        data = snmp_walk(target, cmd)
        resp = parse_str(data, cmd)
        respond_list.append(resp)

    cmd_list = ["dskTotal", "dskUsed", "dskAvail", "dskPercent"]
    for cmd in cmd_list:
        data = snmp_walk(target, cmd)
        resp = parse_int(data, cmd)
        respond_list.append(resp)

    callback = {"warning": False}
    if respond_list:
        print_sys(respond_list, callback)
    else:
        print "Unknown error"

    if callback["warning"]:
        with open("/tmp/snmpdf", "a") as f:
            f.write("\nWarning:\n    No space left on device (" + target + ") soon.\n\n")
        f.close()

        email_user = 'hplan@grandstream.cn'
        email_pwd = 'Dev_1_3614'
        # rcv_list = ['hplan@grandstream.cn', 'gwzhang@grandstream.cn', 'ahluo@grandstream.cn']
        rcv_list = "hplan@grandstream.cn, gwzhang@grandstream.cn, ahluo@grandstream.cn"
        subject = 'Warning: No space left on build server.'

        with open("/tmp/snmpdf", "r") as f:
            content = f.read()
        send_mail(email_user, email_pwd, rcv_list, subject, content)
