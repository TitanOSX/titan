from __future__ import unicode_literals

import datetime
from os import environ
from sys import exit
from os.path import join
from ctznosx import __version__ as version
from titantools import system as s
import urllib2, urllib, httplib, json
from config import ctznConfig

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )

# Get Defaults
software = s.sw_details()
hardware = s.hw_details()

# Log Prefix
PREFIX = "[ Manager::Register ] "

""" register """
def register_device():

    print PREFIX, "Attempting to register device with remote server"
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

    code, resp = send_request("%s/connect/%s" % (CONFIG["reporting"]["target"], data["serial"]), data)
    
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
    try:
        request = urllib2.Request(target, urllib.urlencode(data) )
        request.add_header("User-Agent", "ctznOSX %s" % version)
        opener = urllib2.build_opener()
        response = opener.open(request)
        response_object = response.getcode(), response

    except urllib2.HTTPError, e:
        if e.code == 307:
            print PREFIX, "This device needs to be registered"
            for line in str(e.headers).splitlines():
                if "Location" in line:
                    new_target = line.split(": ", 1)[1]
                    response_object = send_request( new_target, data )
        else:
            response_object = e.code, e.read()

    except urllib2.URLError, e:
        response_object = 0, 'Connection Refused'


    return response_object
