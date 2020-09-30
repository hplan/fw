#!/bin/env python
import requests
import json


rest_api = None


class REQ_INTERFACE:
    Login = 1
    Valid_Login = 2
    Logout = 3
    Bug = 4
    Search = 5
    Update_Bug = 6


def login(url, usr, pwd):
    query = {"login": usr, "password": pwd}
    r = requests.get(url, params=query)
    if 200 <= r.status_code <= 299:
        data = r.json()
        if 'token' in data:
            return data['token']
        else:
            print("login failed, please check your bugzilla configurations.")
            return None
    # elif r.status_code == 401:
    #     print 401


def valid_login(url, user, token):
    query = {"login": user, "token": token}
    r = requests.get(url, params=query)
    if r.status_code == 200:
        data = r.json()
        if data:
            return bool(data['result'])
    return False


def __load_rest_api():
    with open('./rest_api/rest_api.json') as load_f:
        data = json.load(load_f)
        global rest_api
        rest_api = data
    load_f.close()


def get_req_path(req_method):
    if req_method < 0:
        return ""

    if not rest_api:
        __load_rest_api()

    if req_method == REQ_INTERFACE.Login:
        return rest_api['login']
    elif req_method == REQ_INTERFACE.Valid_Login:
        return rest_api['valid_login']
    elif req_method == REQ_INTERFACE.Logout:
        return rest_api['logout']
    elif req_method == REQ_INTERFACE.Bug:
        return rest_api['bug']
    elif req_method == REQ_INTERFACE.Search:
        return rest_api['search']
    elif req_method == REQ_INTERFACE.Update_Bug:
        return rest_api['update-bug']
    else:
        return ""


def comment(url, data):
    requests.post(url, data=data)

