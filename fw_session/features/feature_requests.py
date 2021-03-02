#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fw_session.BugzillaApi
from fw_session.model import DatabaseExecutor as db
import xlrd
import xlwt
import json
from fw_session.model import Bug

executor = db.DatabaseExecutor()
controller = fw_session.BugzillaApi.BugzillaApi()


def filtering(bugs, reporter):
    bs = []
    for bug in bugs:
        if bug.get_creator() != reporter:
            continue
        bs.append(bug)
    return bs


def filtering2(bugs):
    bs = []
    for bug in bugs:
        if bug.get_creator().endswith(".com"):
            bs.append(bug)
    return bs


def run(comments):
    bz = executor.bz_query()
    prods = executor.prod_query()
    if not bz or not prods:
        print "Please continue after your personal information is perfected. "
        exit(0)
    # search security bugs
    bugs = controller.search_bug()
    bugs = bugs[::-1]
    to_json(bugs)
    bugs = to_beans()
    book = xlwt.Workbook()
    fbs = filtering(bugs, "kchguo@grandstream.cn")
    write_excel(book, 'security', fbs, comments)

    # for repo in repos:
    fbs = filtering2(bugs)
    write_excel(book, "features", fbs, comments)

    book.save("demo1.xlsx")


def set_style(name, height, row, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    alignment = xlwt.Alignment()
    alignment.vert = alignment.VERT_CENTER
    alignment.wrap = 1
    style.alignment = alignment
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.font = font
    if row % 2 == 0:
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']
        style.pattern = pattern
    style.borders = borders

    return style


# 写excel
def write_excel(book, sheet, bugs, comments):
    # fr = xlrd.open_workbook("demo1.xlsx")
    # f = copy(fr)
    # row = f.sheet_by_name("security").nrows
    f = book
    '''
    创建第一个sheet:
      sheet1
    '''
    sheet1 = f.add_sheet(sheet, cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'ID', u'Product', u'Component', u'Status', u'Resolution', u'Summary', u'SW Comment',
            u'Create Time', u'Last Change']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Courier New', 220, 2, True))

    row = 1
    for bug in bugs:
        style = set_style('Courier New', 220, row, False)
        sheet1.write(row, 0, bug.get_id(), style)
        sheet1.write(row, 1, bug.get_product(), style)
        sheet1.write(row, 2, bug.get_component(), style)
        sheet1.write(row, 3, bug.get_status(), style)
        sheet1.write(row, 4, bug.get_resolution(), style)
        sheet1.write(row, 5, bug.get_summary(), style)
        sheet1.write(row, 6, comments.get(str(int(bug.get_id()))), style)
        sheet1.write(row, 7, bug.get_creation_time(), style)
        sheet1.write(row, 8, bug.get_last_change_time(), style)

        sheet1.row(row).height_mismatch = True
        sheet1.row(row).height = 40 * 20

        row += 1

    sheet1.col(0).width = 256 * 15
    sheet1.col(1).width = 256 * 15
    sheet1.col(2).width = 256 * 15
    sheet1.col(3).width = 256 * 15
    sheet1.col(4).width = 256 * 15
    sheet1.col(5).width = 256 * 120
    sheet1.col(6).width = 256 * 33
    sheet1.col(7).width = 256 * 33

    # f.save('demo1.xlsx')  # 保存文件


def read_books(datas):
    book = xlrd.open_workbook("demo1.xlsx")
    sheet = book.sheet_by_name("features")
    for i in range(1, sheet.nrows):
        c_cell_id = sheet.cell_value(i, 0)
        c_cell_comment = sheet.cell_value(i, 6)
        datas[str(int(c_cell_id))] = c_cell_comment


def to_json(bugs):
    bug_arr = []
    for bug in bugs:
        t = dict()
        t['id'] = bug.get_id()
        t['product'] = bug.get_product()
        t['component'] = bug.get_component()
        t['status'] = bug.get_status()
        t['resolution'] = bug.get_resolution()
        t['summary'] = bug.get_summary()
        t['creation_time'] = bug.get_creation_time()
        t['last_change_time'] = bug.get_last_change_time()
        t['creator'] = bug.get_creator()
        bug_arr.append(t)

    with open('data.json', 'w') as json_f:
        json_f.write(json.dumps(bug_arr))


def to_beans():
    with open("data.json", "r") as f:
        data = json.load(f)
        ds = []
        for d in data:
            b = Bug.Bug()
            b.set('id', d['id'])
            b.set('product', d['product'])
            b.set('component', d['component'])
            b.set('status', d['status'])
            b.set('resolution', d['resolution'])
            b.set('summary', d['summary'])
            b.set('creator', d['creator'])
            b.set('creation_time', d['creation_time'])
            b.set('last_change_time', d['last_change_time'])
            ds.append(b)
    return ds


if __name__ == '__main__':
    sw_comments = {}
    read_books(sw_comments)
    run(sw_comments)
