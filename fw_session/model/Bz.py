#!/usr/bin/env python
# -*- coding:utf-8 -*-
__metaclass__ = type


class Bz(dict):

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

    def get_host_url(self):
        return getattr(self, "bz_host")

    def get_config_usr(self):
        return getattr(self, "bz_name")

    def get_config_pwd(self):
        return getattr(self, "bz_pwd")

    def get_config_token(self):
        return getattr(self, "bz_token")

    def set_token(self, token):
        setattr(self, "bz_token", token)
