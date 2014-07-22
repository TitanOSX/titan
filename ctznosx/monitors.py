from __future__ import unicode_literals

import getpass
from os import walk
from sys import exit
from shutil import rmtree
from os.path import isdir,join
from titantools.system import shell_out
import urllib2, urllib, httplib, json

MONITOR_PATH = '/var/lib/ctznosx/'

# TODO: Install checksum check on package
def install(args):
    PREFIX = "[ Monitor::Install ] "

    print PREFIX, "Checking for monitor at: %s" % args[0]

    # Check if it's already installed
    if does_monitor_exist(args[0]):
        print PREFIX, "This monitor already exists"       
        exit(2)

    # Check if it's a valid URL
    if 200 == http_get_module(args[0]):
        print PREFIX, "Valid HTTP link, lets install it"
        shell_out("cd %s && sudo git clone %s" % (MONITOR_PATH, args[0]))
        shell_out("sudo chown -R _ctznosx %s" % MONITOR_PATH)

    else:
        print PREFIX, "That is not a valid module, not installing anything"
        exit(1)
    

def does_monitor_exist(monitor):
    # Parse out the monitor from URL assuming Github
    monitor = monitor.rsplit('/', 1)[-1].split(".")[0]

    if isdir(join(MONITOR_PATH, monitor)):
        return True
    else:
        return False 

def remove(args):

    PREFIX = "[ Monitor::Remove ] "

    if getpass.getuser() != 'root':
        print PREFIX, "Please run this with elevated permissions"
        exit(1)
    
    if does_monitor_exist(args[0]):
        rmtree(join(MONITOR_PATH, args[0]))
    else:
        print "Not a valid monitor"
        exit(1)

def list(args):
    for path, dirs, files in walk(path):
      print path
      for f in files:
        print f

# Send the request
def http_get_module( target ):

  try:
    request = urllib2.Request(target)
    opener = urllib2.build_opener()
    response = opener.open(request)
    response_code = response.getcode()

  except urllib2.HTTPError, e:
    if e.code == 307:
      for line in str(e.headers).splitlines():
        if "Location" in line:
          new_target = line.split(": ", 1)[1]
          return send_request( new_target )
    else:
      return e.code
  
  except ValueError, e:
    return 500

  except urllib2.URLError, e:
    return 500

  return response_code    