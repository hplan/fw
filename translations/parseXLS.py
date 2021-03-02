#!/usr/bin/env python
# -*- coding=utf-8 -*-
import xlrd
import collections


INPUT_XLS = "gxv33xx-hebrew_Excel.xlsx"
OUTPUT_EN = "output_en.txt"
OUTPUT_ZH = "output_zh.txt"
OUTPUT_HE = "output_he.txt"


def read_sheet1(en_list, zh_list, excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)

    for rowNum in range(table.nrows):
        if rowNum > 4:
            row = table.row_values(rowNum)
            en_list[int(row[0])] = row[1].encode("utf-8")
            zh_list[int(row[0])] = row[2].encode("utf-8")


def export_lcd_languages():
    en_list = collections.OrderedDict()
    zh_list = collections.OrderedDict()

    read_sheet1(en_list, zh_list, excelFile=excelFile)
    en_list = sorted(en_list.iteritems(), key=lambda x: int(x[0]), reverse=False)
    zh_list = sorted(zh_list.iteritems(), key=lambda x: int(x[0]), reverse=False)

    with open(OUTPUT_ZH, "w+") as f_zh:
        for k, v in zh_list:
            f_zh.write(str(k) + "," + v + '\n')
        pass

    with open(OUTPUT_EN, "w+") as f_en:
        for k, v in en_list:
            f_en.write(str(k) + "," + v + '\n')

    print "Export successfully."


def read_sheet2(excelFile):
    data = xlrd.open_workbook(excelFile)
    # table = data.sheet_by_index(2)
    # with open("web_zh.js", "w+") as f:
    table = data.sheet_by_index(1)
    with open("web_en.js", "w+") as f:
        for rowNum in range(table.nrows):
            row = table.row_values(rowNum)
            line = row[0].encode("utf-8")
            if len(line) == 0:
                continue

            if not line.startswith("/*") and not line.endswith(";"):
                line = line + ";"
            f.write(line + "\n")


def export_web_languages():
    read_sheet2(excelFile=excelFile)


def export_tooltips():
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(4)
    with open("tips_zh.js", "w+") as f:
    # table = data.sheet_by_index(3)
    # with open("tips_en.js", "w+") as f:
        f.write("""function TipsDef(id, content) {
    this.id = id;
    this.content = content;
}


var tip_item_en = new Array;
tip_item_en.push (

    /*account status*/
    /*new TipsDef("Accounts' name",
        "All the SIP accounts on the phone. Each account will show its status on this page."),
    new TipsDef("Number",
        "SIP User ID for the account."),
    new TipsDef("Registered Status",
        "Registration status for the SIP account."),
    new TipsDef("SIP Server",
        "URL or IP address, and port of the SIP server."),*/
        
""")

        for rowNum in range(table.nrows):
            row = table.row_values(rowNum)
            line = row[0].encode("utf-8")
            if len(line) == 0:
                continue

            if not line.startswith("/*") and not line.endswith(","):
                line = line + ","
            f.write("    " + line + "\n")
        f.write(");")


def export_hebrew():
    he_list = collections.OrderedDict()

    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)

    for rowNum in range(table.nrows):
        if rowNum > 4:
            row = table.row_values(rowNum)
            he_list[int(row[0])] = row[4].encode("utf-8")

    he_list = sorted(he_list.iteritems(), key=lambda x: int(x[0]), reverse=False)

    with open(OUTPUT_HE, "w+") as f_zh:
        for k, v in he_list:
            f_zh.write(str(k) + "," + v + '\n')
        pass


if __name__ == '__main__':
    excelFile = INPUT_XLS
    # export_lcd_languages()
    # export_web_languages()
    # export_tooltips()
    export_hebrew()


