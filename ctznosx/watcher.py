#!/usr/bin/env python
#
# Todo: Read config file, use target as test for urlopen2
# Todo: Check to make sure we don't duplicate queue files
#

import sys
import logging
import hashlib
from ctznosx import __version__ as version
from sys import exit
import urllib2, urllib, httplib, json
from os import path,walk,remove,environ
from os.path import dirname, realpath, isfile, join, splitext, basename
from binascii import b2a_hex,hexlify
from config import ctznConfig
from titantools.orm import TiORM as ctznORM
from titantools.system import shell_out,hw_serial as get_device_serial
from zlib import compress
from time import sleep,strftime,strptime,gmtime,mktime

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )

# Set datastore
DATASTORE = CONFIG['main']['datastore']

# Load ORM 
ORM = ctznORM(DATASTORE)

# Set device id
DEVICEID = get_device_serial()

# Create Run Prefix
RUN_PREFIX = "[%s] " % strftime("%a, %d %b %Y %H:%M:%S-%Z", gmtime())

# Load default schema
ORM.initialize_table('watcher', {u'date': {u'nullable': False, u'type': u'text'}, 
                u'utime': {u'type': u'integer'}, 
                u'module': {u'type': u'text'}, 
                u'status': {u'type': u'integer'}})

# Get reporting target
REPORTING_TARGET = "%s%s" % (CONFIG['reporting']['target'], "observer")

if REPORTING_TARGET is None or REPORTING_TARGET == "":
  print "[!] No place to report to"
  exit()


# Check if Watcher is enabled
if CONFIG['watcher']['enabled'] is "false":
  print "[!] Watcher is disabled"
  exit()

# Configure Logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

def generate_reports():

  # Report Timestamp
  unix_time = int(mktime(gmtime()))
  exec_time = strftime("%a, %d %b %Y %H:%M:%S-%Z", gmtime())

  # Query all tables
  all_tables = ORM.select('sqlite_master', 'name',  "type = 'table' and name != 'watcher'")

  # How many wins do we need
  passes_needed = 0
  passes_had = 0

  # Loop through tables
  for table in [table for table in all_tables]:
    # Last success
    last_success = ORM.raw_sql('SELECT * FROM watcher WHERE module="%s" ORDER BY date DESC LIMIT 1' % (table['name']))

    # Get table data
    if len(last_success[0]) is 0:
      # Logging is cool
      temp_utime = unix_time
      ORM.raw_sql("INSERT INTO watcher (date,status,utime,module) VALUES ('%s', 0,'%s', '%s')" % (exec_time, temp_utime, table['name']))
      logging.info("%sCollecting data for [%s] since ever" % (RUN_PREFIX,table['name']))
      results = ORM.select(table['name'], '*')
    else:
      # Logging is cool
      temp_utime = int(last_success[0][4])
      logging.info("%sCollecting data for [%s] since %s" % (RUN_PREFIX,table['name'],last_success[0][1]))
      results = ORM.select(table['name'], '*', 'unixtime > %d' % temp_utime)

    if results is None or len(results) == 0:
      ORM.raw_sql("UPDATE watcher SET status=0, utime = '%d' WHERE module = '%s'" % (unix_time, table['name']))
      continue

    # Dump table to json
    table_json = json.dumps({"module": table['name'], "data": results})

    # Compress the data
    compressed = compress(table_json)

    # Digest
    content_digest = hashlib.sha256(compressed).hexdigest()

    # Send the table data upstream
    target = "%s/%s" % (REPORTING_TARGET, DEVICEID)
    logging.info("\tSending request to '%s'" % target)
    code, response = send_request(target, {'serial': DEVICEID, 'digest': content_digest, 'stream': compressed})
    try:
      logging.info("\tResponse: [%d] @ '%s'" % (code, (response.read())))
    except:
      logging.info("\tResponse: [%d] @ '%s'" % (code, (response)))


    if code == 202:
      passes_had += 1
      ORM.raw_sql("UPDATE watcher SET status=1, utime = %d WHERE module = '%s'" % (unix_time, table['name']))
    else:
      ORM.raw_sql("UPDATE watcher SET status=0, utime = %d WHERE module = '%s'" % (temp_utime, table['name']))

  exit()


# Send the request
def send_request( target, data):

  try:
    request = urllib2.Request(target, urllib.urlencode(data) )
    request.add_header("User-Agent", "ctznOSX %s" % version)
    opener = urllib2.build_opener()
    response = opener.open(request)
    response_object = response.getcode(), response

  except urllib2.HTTPError, e:
    response_object = e.code, e.read()

  except urllib2.URLError, e:
    response_object = 0, 'Connection Refused'

  return response_object


# Run the meat and potatoes
def run():

  # Check if internet is available
  try_count = 0

  while True:

    try:
      target = "%s/%s" % (REPORTING_TARGET, DEVICEID)
      logging.info("%sChecking connectivity to: '%s'" % (RUN_PREFIX,target))
      code, response = send_request(target, {'serial': DEVICEID, 'ping': 'ping'})
    except:
      pass

    if code == 203:
      logging.info("%sWatcher detected a connection " % RUN_PREFIX)
      generate_reports()
    else:
       # Seconds for timeout
      seconds = 3**try_count
      
      # Exceeded max timeout
      if seconds >= 3600:
        exit()

      try_count += 1
      logging.info("%sWatcher did not detect a connection, retrying in %d seconds" % (RUN_PREFIX,seconds))

      # Sleep
      sleep(seconds)     

if __name__ == "__main__":
  run()
