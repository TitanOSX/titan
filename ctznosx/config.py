#!/usr/bin/env python
"""
This is the config for ctznOSX
"""
import ConfigParser, inspect
from os.path import dirname,abspath,join,isfile
from sys import argv,exit

# ctznOSX Configuration
def ctznConfig( config_file, ctznosxpath ):

    # Default Configuration
    config = {
        'main': {
            'debug': False, 
            'datastore': join(ctznosxpath,'ctznosx.db'),
            'logstore': join(ctznosxpath,'logs'),
            'monitorstore': join(ctznosxpath, "monitors"),
            'reportstore': join(ctznosxpath, "reports")
            }, 
        'reporting': {
            'type': 'http', 
            'enabled': False, # True or False 
            'target': ''
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
