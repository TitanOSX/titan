#!/usr/bin/env python
"""
This is the config for titanOSX
"""
import ConfigParser, inspect
from os.path import dirname,abspath,join,isfile
from sys import argv,exit

# titanOSX Configuration
def titanConfig( config_file, titanosxpath ):

    # Default Configuration
    config = {
        'main': {
            'debug': False, 
            'datastore': join(titanosxpath,'titan.db'),
            'logstore': join(titanosxpath,'logs'),
            'monitorstore': join(titanosxpath, "monitors"),
            'reportstore': join(titanosxpath, "reports")
            }, 
        'reporting': {
            'type': 'http', 
            'enabled': False, # True or False 
            'target': '',
            'token': 'default'
            }, 
        'watcher': {
            'enabled': 'true',
            'timeout': 3, # Powers of
            'send_every': 60, 
            }
        }

    if isfile(config_file):
        cp = ConfigParser.ConfigParser()
        cp.read(config_file)
        for section in cp.sections():
            for option in cp.options(section):
                config[section][option] = cp.get(section, option)
    else:
        print '!! NOTICE - Using default configuration'

    return config
