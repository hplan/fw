#!/usr/bin/env python
# -*- coding:utf-8 -*-
__metaclass__ = type


class Product(dict):

    def __init__(self, *args, **kwargs):
        super(dict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = dict(value)
        return value

    def __setattr__(self, key, value):
        self[key] = value

    def set(self, key, value):
        setattr(self, key, value)

    def get(self, key):
        return getattr(self, key)

    def get_product_name(self):
        return getattr(self, "name")

    def get_product_dir(self):
        return getattr(self, "dir")
