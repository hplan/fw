#!/usr/bin/env python
from OpengooApi import OpengooApi
import random
from config import *

def main():
    args = sys.argv
    progname = args[0]
    dirname = os.path.dirname(progname)
    print("dirname is " + dirname)
    sys.path.append(dirname)
    os.chdir(dirname)
    config = check_config(get_config(args))
    og = OpengooApi()

    # login
    uid = login(og, config)

    # get project id
    projectid = get_project_id(og, config)

    print("find project " + config['project'])

    if not config.has_key('module') or not config['module']:
        moduleid = projectid
    else:
        # get module id
        modules = config['module'].split("/")
        findid = projectid
        for module in modules:
            moduleid = get_module_id(og, module, findid)
            findid = moduleid
            print("find module " + module)

    # check filename
    upload_option_id = check_file_name(og, config, moduleid)
    if upload_option_id != -1:
        print("replace already exist file")

    # tmp upload file
    genid = tmp_upload_file(og, config)

    # add file to module
    fileid = add_file_to_module(og, config, genid, moduleid, uid, upload_option_id)

    print('add file to ' + config.get('project', '') + '/' + config.get('module', '') + ' done')
    print("")
    print("")
    print_info(config['remotename'] + ':  https://115.236.68.174:8888/fengoffice_new/index.php?c=files&a=download_file&id=' + str(fileid))


def login(og, config):
    loginr = og.login(config['user'], config['password'])
    check_expect(loginr.status_code, 200, loginr, 'login failed!')
    check_not_expect(loginr.cookies.get('https___192_168_120_248_fengoffice_newtoken'), None, loginr, 'login failed!')
    check_not_expect(loginr.cookies.get('https___192_168_120_248_fengoffice_newid'), None, loginr, 'login failed!')
    print('login use ' + config['user'] + " success")
    uid = loginr.cookies.get('https___192_168_120_248_fengoffice_newid')
    return uid

def get_project_id(og, config):
    dimenr = og.getdimenProjects("1")
    err_msg = 'get dimen failed!'
    check_expect(dimenr.status_code, 200, dimenr, err_msg)
    check_not_expect(dimenr.content, None, dimenr, err_msg)
    projects_response = parse_json_in_str(dimenr.content)

    if not 'dimension_members' in projects_response:
        print_err('unexpect projects response with ' + projects_response)
        exit(-3)

    dimens = projects_response['dimension_members']
    projectid = find_project_id(dimens, config['project'])
    if projectid <= 0:
        print_err("failed to find project " + config['project'] + " in Opengoo!!!")
        exit(-4)
    return projectid

def get_module_id(og, module, projectid):
    moduler = og.getmemberchilds(str(projectid))
    err_msg = 'get module info failed!!!'
    check_expect(moduler.status_code, 200, moduler, err_msg)
    check_not_expect(moduler.content, None, moduler, err_msg)
    module_response = parse_json_in_str(moduler.content)
    modules = module_response['members']
    moduleid = find_module_id(modules, module)
    if moduleid <= 0:
        print_err("failed to find module " + module + " in Opengoo!!!")
        exit(-4)
    return moduleid


def check_file_name(og, config, moduleid):
    cfnr = og.checkfilename(moduleid, config['remotename'])
    err_msg = 'check filename failed!!!'
    check_expect(cfnr.status_code, 200, cfnr, err_msg)
    check_not_expect(cfnr.content, None, cfnr, err_msg)

    upload_option_id = -1
    cfnr_response = parse_json_in_str(cfnr.content)
    if 'files' in cfnr_response:
        # has same name file, update it
        upload_option_id = cfnr_response['files'][0]['id']

    return upload_option_id


def tmp_upload_file(og, config):
    random.seed()
    rand1 = int(random.random()*10000000)
    random.seed()
    rand2 = int(random.random()*10000)
    genid = 'og_' + str(rand1) + '_' + str(rand2)
    #print('genid is ' + genid)

    print('start upload file ' + config['localpath'] + ' to ' + config['remotename'])
    print_info('in uploading ... please wait. file size ' + get_file_size(config['localpath']))
    tufr = og.tmpuploadfile(genid, config['localpath'], config['remotename'])
    err_msg = 'upload file failed!!!'
    check_expect(tufr.status_code, 200, tufr, err_msg)
    check_not_expect(tufr.content, None, tufr, err_msg)
    print('upload file ' + config['localpath'] + ' complete')
    return genid


def add_file_to_module(og, config, genid, moduleid, uid, upload_option_id):
    amfr = og.addmultifile(genid, config['remotename'], moduleid, uid, upload_option_id, config['desc'])
    err_msg = 'add file to project failed!!!'
    check_expect(amfr.status_code, 200, amfr, err_msg)
    check_not_expect(amfr.content, None, amfr, err_msg)
    amfr_response = parse_json_in_str(amfr.content)
    if not 'errorCode' in amfr_response or not 'file' in amfr_response:
        print_err('error add file response with ' + amfr_response)
        exit(-5)

    if amfr_response['errorCode'] != 0:
        print_err('error add file response code :' + amfr_response['errorCode'])
        exit(-5)

    print(amfr_response['errorMessage'])
    projectfile = amfr_response['file'][0]
    return projectfile.split(':')[1]

def check_expect(real, expect, r, msg):
    if real != expect:
        print_err('error result ' + str(real) + ", while expect " + str(expect) + " in " + str(r))
        if msg is not None:
            print_err(msg)
        exit(-2)

def check_not_expect(real, expect, r, msg):
    if real == expect:
        print_err('error not expect result ' + str(real) + " in " + str(r))
        if msg is not None:
            print_err(msg)
        exit(-2)


if __name__ == '__main__':
    main()


