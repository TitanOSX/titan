from __future__ import unicode_literals
from titantools.system import shell_out
import urllib2, urllib, httplib, json

# TODO: Install checksum check on package
def install(args):
    PREFIX = "[ Monitor::Install ] "
    print PREFIX, "Checking for monitor at: %s" % args[0]
    if 200 == http_get_module(args[0]):
        print PREFIX, "Valid HTTP link, lets check it out"
    else:
        print PREFIX, "That is not a valid module"
    #sys("git %s /var/lib/ctznosx/monitors/")
    

def remove(args):
    print args

# Send the request
def http_get_module( target ):

  try:
    request = urllib2.Request(target)
    opener = urllib2.build_opener()
    response = opener.open(request)
    response_object = response.getcode(), response

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

  return response_object    