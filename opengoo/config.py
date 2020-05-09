#!/usr/bin/env python

from utils import *
import logging, os
import getopt

config_path = 'config.json'
helpinfo = '''
    -h show this information
    -v show version info
    -u set username
    -w set password
    -l set local file path to upload
    -r set remote file name
    -p set project name like WP800/GXV3370/GVC3210 in opengoo workspace
    -m set module name like Dev,Doc,Firmware use / for more module levels like GXV3370/Doc 
'''

version = '1.0.1'

def get_config(args):
    config = {}
    with open(config_path, 'rb') as f:
            try:
                config = parse_json_in_str(remove_comment(f.read().decode('utf8')))
            except ValueError as e:
                logging.error('found an error in config.json: %s', str(e))
                sys.exit(1)

    if not config.has_key('desc'):
        config['desc'] = '-- Initial version by script --'

    shortopt = 'hvp:m:l:r:u:w:d:'
    optlist, arg = getopt.getopt(args[1:], shortopt)
    for key, value in optlist:
        if key == '-h':
            print(helpinfo)
            exit(0)
        elif key == '-v':
            print(version)
            exit(0)
        elif key == '-p':
            config['project'] = value
        elif key == '-m':
            config['module'] = value
        elif key == '-l':
            config['localpath'] = value
        elif key == '-r':
            config['remotename'] = value
        elif key == '-u':
            config['user'] = value
        elif key == '-w':
            config['password'] = value
        elif key == '-d':
            config['desc'] = value
        else:
            continue
    #print(config)
    return config

def check_config(config):
    if len(config) == 0:
        print('error! config is empty')
        exit(-1)

    if not config.has_key('user') or not config['user']:
        print('error! user is empty')
        exit(-1)

    if not config.has_key('password') or not config['password']:
        print('error! password is empty')
        exit(-1)

    if not config.has_key('localpath') or not config['localpath']:
        print('error! localpath is empty')
        exit(-1)

    if not os.access(config['localpath'], os.R_OK):
        print('error! cannot read ' + config['localpath'])
        exit(-1)

    if not config.has_key('project') or not config['project']:
        print('error! project is empty')
        exit(-1)

    if not config.has_key('remotename') or not config['remotename']:
        config['remotename'] = config['localpath'].split('/')[-1]

    #print(config)
    return config
