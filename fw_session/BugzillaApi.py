#!/bin/env python
import rest_api.bugzilla_api as bugzilla_api
import requests
import ConfigParser
import model.DatabaseExecutor as model
executor = model.DatabaseExecutor()


class BugzillaApi:
    def __init__(self):
        self.bz = executor.bz_query()
        self.host = self.bz.get_host_url()
        self.user = self.bz.get_config_usr()
        self.token = self.bz.get_config_token()
        self.pwd = self.bz.get_config_pwd()
        config = ConfigParser.ConfigParser()
        config.readfp(open('./.product.ini'))
        self.product_id = config.getint("product_section", "product_id")
        self.product = executor.get_product(self.product_id)

    def load_cfg(self):
        self.bz = executor.bz_query()
        self.host = self.bz.get_host_url()
        self.user = self.bz.get_config_usr()
        self.token = self.bz.get_config_token()
        self.pwd = self.bz.get_config_pwd()
        config = ConfigParser.ConfigParser()
        config.readfp(open('./.product.ini'))
        self.product_id = config.getint("product_section", "product_id")
        self.product = executor.get_product(self.product_id)

    def do_login(self):
        valid_path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Valid_Login)
        url = self.host + "/" + valid_path
        # valid login
        if bugzilla_api.valid_login(url, self.user, self.token):
            print "token valid"
            return
        else:
            print "exists token was invalid. request login..."

        # obtain new token
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Login)

        url = self.host + "/" + path
        print "url: " + url
        tk = bugzilla_api.login(url, self.user, self.pwd)
        if tk:
            self.bz.set_token(tk)
            executor.bz_update(self.bz)

    def get_bug_info(self, bug_id):
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Bug) % str(bug_id)
        url = self.host + "/" + path

        query = {"token": self.token}
        r = requests.get(url, params=query)
        if r.status_code == 200:
            data = r.json()
            status = data['bugs'][0]['status']
            resolution = data['bugs'][0]['resolution']
            bug_id = data['bugs'][0]['id']
            summary = data['bugs'][0]['summary']
            print "%8s %8s [Bug %s] %s" % (status, resolution, bug_id, summary)
        elif r.status_code == 401:
            self.do_login()
            self.load_cfg()
            self.get_bug_info(bug_id)

    def get_bugs_info(self, bug_ids):
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Search)
        url = self.host + "/" + path
        query = {
            "id": bug_ids,
            "token": self.token
        }
        r = requests.get(url, params=query)
        if r.status_code == 200:
            data = r.json()
            if data:
                for d in data['bugs']:
                    product = d['product']
                    if product != self.product.get_product_name():
                        continue
                    status = d['status']
                    resolution = d['resolution']
                    bug_id = d['id']
                    summary = d['summary']
                    print "%10s %10s %10s [Bug %s] %s" % (product, status, resolution, bug_id, summary)
                print("\n")
                print " total: %d" % len(data['bugs'])
            return data
        elif r.status_code == 401:
            self.do_login()
            self.load_cfg()
            self.get_bugs_info(bug_ids)
#        return data

    def get_release_note(self):
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Search)
        url = self.host + "/" + path
        query = {
            "token": self.token,
            "product": self.product.get_product_name(),
            "resolution": "FIXED",
            "status": "RESOLVED",
        }
        r = requests.get(url, params=query)
        if r.status_code == 200:
            data = r.json()
            bugs = data['bugs']
            if bugs:
                bug_ids = []
                for b in bugs:
                    bug_ids.append(b['id'])
                    print " [Bug %s] %s" % (b['id'], b['summary'])
                print "\n"
                print " total: %d" % len(bugs)
                return bug_ids
        elif r.status_code == 401:
            self.do_login()
            self.load_cfg()
            self.get_release_note()

    def comment(self, bug_id, comment):
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Update_Bug)
        path = path % bug_id
        url = self.host + "/" + path
        data = {
            "token": self.token,
            "comment": comment
        }
        print url
        r = requests.post(url, data=data)
        print r.json()

    def get_comment(self, bug_id):
        path = bugzilla_api.get_req_path(bugzilla_api.REQ_INTERFACE.Update_Bug)
        path = path % bug_id
        url = self.host + "/" + path
        query = {
            "token": self.token
        }
        data = requests.get(url, params=query)
        print data.json()
