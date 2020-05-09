#!/usr/bin/env python


import json
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

class JSFormat:
    def __init__(self):
        self.state = 0

    def push(self, ch):
        ch = ord(ch)
        if self.state == 0:
            if ch == ord('"'):
                self.state = 1
                return to_str(chr(ch))
            elif ch == ord('/'):
                self.state = 3
            else:
                return to_str(chr(ch))
        elif self.state == 1:
            if ch == ord('"'):
                self.state = 0
                return to_str(chr(ch))
            elif ch == ord('\\'):
                self.state = 2
            return to_str(chr(ch))
        elif self.state == 2:
            self.state = 1
            if ch == ord('"'):
                return to_str(chr(ch))
            return "\\" + to_str(chr(ch))
        elif self.state == 3:
            if ch == ord('/'):
                self.state = 4
            else:
                return "/" + to_str(chr(ch))
        elif self.state == 4:
            if ch == ord('\n'):
                self.state = 0
                return "\n"
        return ""

def remove_comment(json):
    fmt = JSFormat()
    return "".join([fmt.push(c) for c in json])


def parse_json_in_str(data):
    # parse json and convert everything from unicode to str
    return json.loads(data, object_hook=_decode_dict)


def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def find_project_id(response, proname):
    for project in response:
        if project['name'] == proname:
            return project['id']
    return 0

def find_module_id(response, modulename):
    for module in response:
        if module['name'] == modulename:
            return module['id']
    return 0

def get_file_size(path):
    size = os.path.getsize(path)
    rsize = size
    unit = ' B'
    ksize = size/float(1024)
    if ksize > 1:
        unit = ' KB'
        rsize = ksize
    else:
        return str(rsize) + unit

    msize = ksize/float(1024)
    if msize > 1:
        unit = ' MB'
        rsize = msize
    else:
        return str(rsize) + unit

    gsize = msize/float(1024)
    if gsize > 1:
        unit = ' GB'
        rsize = gsize

    return str(rsize) + unit


def print_err(msg):
    print("\033[0;31;42m" + msg + "\033[0m")

def print_info(msg):
    print("\033[0;34m" + msg + "\033[0m")

