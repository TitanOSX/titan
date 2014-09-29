import json
import hashlib
import requests

from titanosx import __version__ as version

# Set titanOSX headers
HEADERS = { 'User-Agent': "titanOSX %s" % version }

def post(url, data=None):
    r = requests.post(url, data=data, headers=HEADERS)
    print r

def get(url):
    pass

def put():
    pass

def delete():
    pass

# Send the request
def check_connectivity( target ):
  try:
    request = urllib2.Request( target )
    request.add_header("User-Agent", "titanOSX %s" % version)
    opener = urllib2.build_opener()
    response = opener.open(request, timeout = 1)
    response_object = response.getcode(), response
    logging.info(response_object)
  except urllib2.HTTPError, e:
    response_object = e.code, e.read()

  except urllib2.URLError, e:
    response_object = 0, 'Connection Refused'

  return response_object
