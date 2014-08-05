from __future__ import unicode_literals

import datetime
from os import environ
from sys import exit
from os.path import join
from titantools.system import shell_out
import urllib2, urllib, httplib, json
from config import ctznConfig

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )

""" register """
def regiter(args):
    PREFIX = "[ Manager::Register ] "
    print PREFIX, "Attempting to register device with remote server"
