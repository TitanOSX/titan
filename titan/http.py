import json
import hashlib
import requests

from titan import __version__ as version

# Set titanOSX headers
HEADERS = { 'User-Agent': "titanOSX %s" % version }

def request(url, data=None, type=None):
  r = None
  try:
    if data is not None:
      r = post(url, data)
    
    else:
      if type is None:
        r = get(url)
      else:
        getattr(type)(*args, **kwargs)

  except requests.exceptions.ConnectionError, e:
    return 0, "A connection could not be established"
  except requests.exceptions.HTTPError, e:
    return e
  except requests.exceptions.RequestException, e:
    pass

def post(url, data=None):
    r = requests.post(url, data=data, headers=HEADERS)
    return r

def get(url):
    r = requests.get(url, headers=HEADERS)
    return r

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
