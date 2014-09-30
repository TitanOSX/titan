from __future__ import unicode_literals

import datetime
from os import environ
from sys import exit
from os.path import join
from titan import __version__ as version, http
from titantools import system as s
import urllib2, urllib, httplib, json
from config import titanConfig

# Get titanOSX Env and Config
TITAN_PATH = (environ.get('TITAN_CONFIG_PATH') or '/var/lib/titanosx/')
TITAN_CONFIG = join('/etc/', 'titan.conf')

# Config
CONFIG = titanConfig( TITAN_CONFIG, TITAN_PATH )

# Get Defaults
software = s.sw_details()
hardware = s.hw_details()

# Log Prefix
PREFIX = "[ Manager::Register ] "

# Reporting Token
TOKEN = {'token': CONFIG['reporting']['token']}

""" check status """
def status():
    print PREFIX, "Checking status for remote server"
    code, resp = http.request("%s/status/%s" % (CONFIG["reporting"]["target"], data["serial"]))
    print resp

""" register """
def register():
    print PREFIX, "Attempting to register device with remote server"

    # Create empty data objects
    data = {}

    data["serial"] = hardware["serial_number"]
    data["uuid"] = hardware["hardware_uuid"]
    data["make"] = hardware["machine_make"]
    data["model"] = hardware["model_short"]
    data["cpu_type"] = hardware["cpu_type"]
    data["cpu_speed"] = hardware["cpu_speed"]
    data["physical_memory"] = hardware["physical_memory"]
    data["os_version"] = software["os_version"]
    data["os_build"] = software["os_build"]

    # Check status first, autoredirect to register
    code, resp = send_request("%s/status/%s" % (CONFIG["reporting"]["target"], data["serial"]), data)
    
    if code == 0:
        print PREFIX, "Unable To Communicate With Registration Server"
        return False
    
    elif code == 304:
        print PREFIX, "Device already registered"
        return True

    elif code == 200:
        print PREFIX, "Device Registered Successfully"
        return True

    else:
        print PREFIX, "Registration Failed, Error: %d - '%s'" % (code, response)
        return False


def send_request( target, data):
    return http.request(target, data)
