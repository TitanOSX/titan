from __future__ import unicode_literals

import datetime
import json
from os import environ
from sys import exit
from os.path import join
from titan import __version__ as version, http
from titantools import system as s
import urllib2, urllib, httplib, json
from config import titanConfig

# Get titanOSX Env and Config
TITAN_PATH = (environ.get('TITAN_PATH') or '/var/lib/titan/')
TITAN_CONFIG = join('/etc/', 'titan.conf')

# Config
CONFIG = titanConfig( TITAN_CONFIG, TITAN_PATH )

# Get Defaults
software = s.sw_details()
hardware = s.hw_details()

# Reporting Token
TOKEN = {'token': CONFIG['reporting']['token']}

# Create empty data objects
data = {}
data["serial"] = hardware["serial_number"]

""" check status """
def status():
    # Log Prefix
    PREFIX = "[ Manager::Status ] "
    print PREFIX, "Checking status for remote server"
    
    code, resp = http.request("%s/api/status/%s" % (CONFIG["reporting"]["target"], data["serial"]))
    
    if code == 0:
        print PREFIX, "Unable To Communicate With Registration Server"
        return False
    
    elif code == 200:
        print PREFIX, "Device is registered with", CONFIG["reporting"]["target"]
        device = json.loads(resp)
        print ""
        print "Remote ID: %s" % device['id']
        print "Serial: %s" % device['serial']
        print "This device is a %s %s with an %s @ %s and %s of memory running %s" % (device['make'], device['model'], device['cpu_type'], device['cpu_speed'], device['physical_memory'], device['os_version'])

    else:
        print PREFIX, "Device is not registered"

""" check status """
def unregister():
    # Log Prefix
    PREFIX = "[ Manager::Unregister ] "
    print PREFIX, "Checking status for remote server"
    
    code, resp = http.request("%s/api/unregister/%s" % (CONFIG["reporting"]["target"], data["serial"]), type='delete')

    if code == 0:
        print PREFIX, "Unable To Communicate With Registration Server"
        return False
    
    elif code == 410:
        print PREFIX, "Unregistered Successfully"
    
    elif code == 404:
        print PREFIX, "Device not registered"

    else:
        print PREFIX, "Error"


"""
Proposed work flow:

register command reaches out to status, if register, return 304
if not, follow 307 redirect, and register, return 200

"""

""" register """
def register():
    # Log Prefix
    PREFIX = "[ Manager::Register ] "
    print PREFIX, "Attempting to register device with remote server"

    data["uuid"] = hardware["hardware_uuid"]
    data["make"] = hardware["machine_make"]
    data["model"] = hardware["model_short"]
    data["cpu_type"] = hardware["cpu_type"]
    data["cpu_speed"] = hardware["cpu_speed"]
    data["physical_memory"] = hardware["physical_memory"]
    data["os_version"] = software["os_version"]
    data["os_build"] = software["os_build"]

    # Check status first, autoredirect to register
    code, resp = send_request("%s/api/status/%s" % (CONFIG["reporting"]["target"], data["serial"]), data)
    
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
        print PREFIX, "Registration Failed, Error: %d - '%s'" % (code, resp)
        return False


def send_request( target, data):
    return http.request(target, data)
