#!/usr/bin/env python
import requests
import mimetypes

class OpengooApi:
    def __init__(self):
        self.default_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0; Gecko/20100101 Firefox/58.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}
        self.default_url = 'https://192.168.120.248/fengoffice_new/index.php'
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)
        self.session.verify = False

    def login(self, user, pwd, configOptionSelect='Default', remember='checked'):
        # https://192.168.120.248/fengoffice_new/index.php?c=access&a=login
        r = self.session.post(self.default_url, params = {'c':'access','a':'login'}, data={'login[username]':user,
                'login[password]':pwd, 'configOptionSelect': configOptionSelect, 'login[remember]':remember})
        return r

    def init(self):
        #https://192.168.120.248/fengoffice_new/index.php?context={}&currentdimension=0&ajax=true&c=files&a=init
        r = self.session.post(self.default_url, params = {'context':'{}','currentdimension':'0','ajax':'true','c':'files','a':'init'})
        return r

    def loaddimeninfo(self):
        # https://192.168.120.248/fengoffice_new/index.php?context=\{\}&ajax=true&currentdimension=0&c=dimension&a=load_dimensions_info
        r = self.session.post(self.default_url, params = {'context':'{}','currentdimension':'0','ajax':'true','c':'dimension','a':'load_dimensions_info'})
        return r

    def getdimenProjects(self, dimenid):
        #https://192.168.120.248/fengoffice_new/index.php?c=dimension&ajax=true&a=initial_list_dimension_members_tree_root&dimension_id=1&avoid_session=1&limit=100
        r = self.session.post(self.default_url, params = {'c':'dimension','a':'initial_list_dimension_members_tree_root','dimension_id':str(dimenid),
                                                          'avoid_session':'1', 'ajax':'true','limit':'100'})
        return r

    def getmemberchilds(self, memberid):
        #https://192.168.120.248/fengoffice_new/index.php?context=\{%221%22:\[0\],%222%22:\[0\]\}&currentdimension=0&ajax=true&c=dimension&a=get_member_childs&member=533&limit=100&offset=0
        r = self.session.post(self.default_url, params = {'context':'{"1":[0],"2":[0]}','currentdimension':'0','c':'dimension',
                                                          'a':'get_member_childs', 'ajax':'true','member':str(memberid), 'limit':'100','offset':'0'})
        return r

    def checkfilename(self, memberid, remotename):
        #check filename
        # https://192.168.120.248/fengoffice_new/index.php?context={"1":[0,1217],"2":[0]}&currentdimension=1&ajax=true&c=files&a=check_filename&id=0&current=1217
        contextstr = '{\"1\":[0,\"' + str(memberid) + '],\"2\":[0]}'
        r = self.session.post(self.default_url, params = {'context': contextstr, 'currentdimension':'1', 'c': 'files', 'ajax':'true',
                                                          'a':'check_filename', 'id': '0', 'current':str(memberid)},
                               data={'members':'[' + str(memberid) + ']', 'filename':remotename})
        return r

    def tmpuploadfile(self, genid, localpath, remotename):
        # tmply add file
        #https://192.168.120.248/fengoffice_new/index.php?&c=files&a=temp_file_upload&id=og_1516933330_518465&upload=true

        type = mimetypes.guess_type(localpath)[0]
        filedata = {'file_file[]':(remotename, open(localpath, 'rb'), type)}
        r = self.session.post(self.default_url, params = {'c':'files','a':'temp_file_upload', 'id': genid,
                                                          'upload':'true'}, files=filedata)
        return r

    def addmultifile(self, genid, remotename, memberid, uid, option=-1, desc='-- Initial version by script --'):
        # judge r ok
        # add multi file
        #https://192.168.120.248/fengoffice_new/index.php?context={"1":[0,1217],"2":[0]}&currentdimension=1&ajax=true&c=files&a=add_multiple_files
        param_rg = genid + '_rg'
        contextstr = '{\"1\":[0,\"' + str(memberid) + '],\"2\":[0]}'
        data = {'modal':'1','':'145','file[add_type]':'regular','file[file_id]':'','file[type]':'','file[upload_id]':genid,
                param_rg:'0','file_file[0]':'C:\\fakepath\\'+remotename,'file[url]':'','file[name]':remotename,
                'file[upload_option]':str(option),'file[revision_comment]': desc,'members':'['+str(memberid)+']',
                'custom_prop_names[0]':'','custom_prop_values[0]':'','original_subscribers':str(uid),'file[attach_to_notification]':'0',
                'file[notify_myself_too]':'1','file[default_subject_sel]':'default','file[default_subject_text]':'','file[description]':'', 'subscribers[user_'+ str(uid) + ']':'1'}
        r = self.session.post(self.default_url, params = {'context':contextstr,'currentdimension':'1', 'ajax':'true','c': 'files',
                                                          'a':'add_multiple_files'}, data=data)
        return r



