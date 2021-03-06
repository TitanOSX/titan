import json
import hashlib
import requests

from os import environ
from os.path import join
from titan import __version__ as version
from config import titanConfig

# Get titanOSX Env and Config
TITAN_PATH = (environ.get('TITAN_PATH') or '/var/lib/titan/')
TITAN_CONFIG = join('/etc/', 'titan.conf')

# Config
CONFIG = titanConfig( TITAN_CONFIG, TITAN_PATH )

# Set titanOSX headers
HEADERS = { 
            "User-Agent": "titanOSX %s" % version, 
            "X-Titan-Token": CONFIG['reporting']['token'] 
          }

def request(url, data=None, type=None):
  r = None
  try:
    if data is not None:
      r = post(url, data)
    
    else:
      if type is None:
        r = get(url)
      else:
        r = globals()[type](url)


    if r is not None and r.status_code == 402:
        print ":: API TOKEN REQUIRED"
        exit()

    return r.status_code, r.content

  except requests.exceptions.ConnectionError, e:
    return 0, "A connection could not be established"
  
  except requests.exceptions.HTTPError, e:
    return e.status, e.message

  except requests.exceptions.RequestException, e:
    return 0, e.message

""" POST Method """
def post(url, data=None):
    r = requests.post(url, data=data, headers=HEADERS)
    return r

""" GET Method """
def get(url):
    r = requests.get(url, headers=HEADERS)
    return r

""" PUT Method """
def put(url):
    r = requests.put(url, headers=HEADERS)
    return r

""" DELETE Method """
def delete(url):
    r = requests.delete(url, headers=HEADERS)
    return r