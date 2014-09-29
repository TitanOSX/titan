#!/usr/bin/env python

import sys
import http
import logging

from sys import exit
from zlib import compress
from config import titanConfig
from binascii import b2a_hex,hexlify
from os import path,walk,remove,environ
from titanosx import __version__ as version
from titantools.orm import TiORM as ctznORM
from time import sleep,strftime,strptime,gmtime,mktime
from titantools.system import shell_out,hw_serial as get_device_serial
from os.path import dirname, realpath, isfile, join, splitext, basename

# Get titanOSX Env and Config
TITAN_PATH = (environ.get('TITAN_PATH') or '/var/lib/titanosx/')
TITAN_CONFIG = join('/etc/', 'titanosx.conf')

# Config
CONFIG = titanConfig( TITAN_CONFIG, TITAN_PATH )

# Set datastore
DATASTORE = CONFIG['main']['datastore']

# Load ORM 
ORM = ctznORM(DATASTORE)

# Set device id
DEVICEID = get_device_serial()

# Create Run Prefix
RUN_PREFIX = "[%s] " % strftime("%a, %d %b %Y %H:%M:%S-%Z", gmtime())

# Reporting Token
TOKEN = {'token': CONFIG['reporting']['token']}

# Load default schema
ORM.initialize_table('watcher', {u'date': {u'nullable': False, u'type': u'text'}, 
                u'utime': {u'type': u'integer'}, 
                u'module': {u'type': u'text'}, 
                u'status': {u'type': u'integer'}})

# Check if a reporting target is set
if CONFIG['reporting']['target'] is None or CONFIG['reporting']['target'] == "":
  print "[!] No place to report to"
  exit()

# Get reporting tarsget
REPORTING_TARGET = "%s%s" % (CONFIG['reporting']['target'], "observer")

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
    http.post(target, {'serial': DEVICEID, 'digest': content_digest, 'stream': compressed})
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


# Run the meat and potatoes
def run():
  # Check if internet is available
  try_count = 0
  code = 0

  # Start infinity loop
  while True:

    # Check connectivity
    try:
      target = "%s/%s" % (REPORTING_TARGET, DEVICEID)
      logging.info("%sChecking connectivity to: '%s'" % (RUN_PREFIX,target))
      code, response = http.check_connectivity(target)
    except:
      pass

    # If CDM returns a 203, send up the reports
    if code == 203:
      logging.info("%sWatcher detected a connection " % RUN_PREFIX)
      generate_reports()
    
    else:
       # Seconds for timeout
      seconds = 2**try_count
      
      # Exceeded max timeout
      if seconds >= 2047:
        exit()

      try_count += 1
      logging.info("%sWatcher did not detect a connection, retrying in %d seconds" % (RUN_PREFIX,seconds))

      # Sleep
      sleep( seconds )     

if __name__ == "__main__":
  run()
