#!/usr/bin/env python
"""
This is the config for Titan
"""
import ConfigParser, inspect
from os.path import dirname,abspath,join,isfile
from sys import argv,exit

# Set the titan directory
TITAN_DIR = dirname(dirname(abspath(inspect.getfile(inspect.currentframe()))))

# Titan Configuration
def TiConfig( config_file ):

    # Default Configuration
    config = {
        'main': {
            'debug': 'true', 
            'datastore': join(TITAN_DIR,'db'),
            'logstore': join(TITAN_DIR,'logs'),
            'modulestore': join(TITAN_DIR, "modules"),
            'reportstore': join(TITAN_DIR, "reports/")
            }, 
        'reporting': {
            'type': 'syslog|http', 
            'enabled': False, # True or False 
            'target': 'http://localhost:9393/ctznOSX'
            }, 
        'watcher': {
            'enabled': 'true',
            'timeout': 10,
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
        exit('Failed to load ctznOSX configuration')

    return config
