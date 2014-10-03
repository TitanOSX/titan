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

    return r.status_code, r.content

  except requests.exceptions.ConnectionError, e:
    return 0, "A connection could not be established"
  except requests.exceptions.HTTPError, e:
    return e.status, e.message
  except requests.exceptions.RequestException, e:
    return e.status, e.message

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
