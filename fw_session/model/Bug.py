#!/usr/bin/env python
# -*- coding:utf-8 -*-
__metaclass__ = type


class Bug(dict):

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

    def get_id(self):
        return getattr(self, "id")

    def get_product(self):
        return getattr(self, "product")

    def get_status(self):
        return getattr(self, "status")

    def get_component(self):
        return getattr(self, "component")

    def get_summary(self):
        return getattr(self, "summary")

    def get_resolution(self):
        return getattr(self, "resolution")

    def get_creator(self):
        return getattr(self, "creator")

    def get_creation_time(self):
        return getattr(self, "creation_time")

    def get_last_change_time(self):
        return getattr(self, "last_change_time")
