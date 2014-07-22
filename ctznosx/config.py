#!/usr/bin/env python
"""
This is the config for Titan
"""
import ConfigParser, inspect
from os.path import dirname,abspath,join,isfile
from sys import argv,exit

# Titan Configuration
def TiConfig( config_file, ctznosxpath ):

    # Default Configuration
    config = {
        'main': {
            'debug': False, 
            'datastore': join(ctznosxpath,'ctznosx.db'),
            'logstore': join(ctznosxpath,'logs'),
            'modulestore': join(ctznosxpath, "monitors"),
            'reportstore': join(ctznosxpath, "reports")
            }, 
        'reporting': {
            'type': 'http', 
            'enabled': False, # True or False 
            'target': 'http://localhost:9393/ctznOSX'
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
