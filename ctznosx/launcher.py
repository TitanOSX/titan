#!/usr/bin/env python
"""
This is the launcher for ctznOSX/Titan
"""

import logging
from sys import argv,exit
from itertools import chain
from config import ctznConfig
from titantools.system import hw_serial as get_device_serial
from socket import gethostname
from time import time, strftime, gmtime
from collections import namedtuple
from subprocess import Popen, PIPE
from os import listdir,walk,path,environ
from os.path import dirname, realpath, isfile, join, splitext, basename

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )

# Configurations
logging.basicConfig(format='%(message)s', level=logging.INFO)

# Constants
CURRENT_DIR = dirname(realpath(__file__))

# Base Modules Dir
MODULES_DIR = CONFIG['main']['monitorstore']

# Log Directory
LOG_DIR = CONFIG['main']['logstore']

# Log Directory
DATASTORE = CONFIG['main']['datastore']

# Report Directory
REPORT_DIR = CONFIG['main']['reportstore']

# Get Hostname
HOSTNAME = gethostname()

# Get Serial Number
SERIALNUMBER = get_device_serial()

# Get Runtime
DATE = strftime("%Y-%m-%dT%H:%M:%S%z", gmtime())

# Define Module Packs
MODULE_PACKS = [
    join(MODULES_DIR, mod_pack) for mod_pack in listdir(MODULES_DIR)
]

# Define all of our modules
MODULES = []
for path in MODULE_PACKS:
    for root,dirs,files in walk(path):
        for f in (f for f in files if f not in [".gitkeep", "README", "schema.py", "config.json"]):
            MODULES.append( join(root,f) )

# Types
CtznLanguage = namedtuple("CtznLanguage", "supported_extensions execution_string")

PYTHON_LANGUAGE = CtznLanguage(
    supported_extensions = [".py", ".pyc"],
    execution_string = "python",
)

RUBY_LANGUAGE = CtznLanguage(
    supported_extensions = [".rb"],
    execution_string = "ruby"
)

BASH_LANGUAGE = CtznLanguage(
    supported_extensions = [".bash", ".sh"],
    execution_string = "/bin/bash"
)

PHP_LANGUAGE = CtznLanguage(
    supported_extensions = [".php"],
    execution_string = "php"
)

PERL_LANGUAGE = CtznLanguage(
    supported_extensions = [".pl"],
    execution_string = "perl"
)

SUPPORTED_LANGUAGES = [
    PYTHON_LANGUAGE,
    RUBY_LANGUAGE,
    BASH_LANGUAGE,
    PHP_LANGUAGE,
    PERL_LANGUAGE,
]

# Set Debugging
testing_enabled = False

if "--verbose" in argv[1:]:
    testing_enabled = True

# Functions
def log_line(log_name, line):
    """log_line accepts a line a returns a properly formatted log line"""
    return "%s %s by[%s]: %s" % (
        DATE,
        HOSTNAME,
        log_name,
        line,
    )

# Spawn module, capture output
def spawn_module(module, current_lang, mod_name):
    """spawn_module executes an individual Titan module"""
    log_file = join(LOG_DIR, mod_name + ".log")
    
    if testing_enabled:
        logging_passthru = '--log'
    else:
        logging_passthru = ''

    command = list(chain(
        ["/usr/bin/sudo"], #/usr/bin/sudo -u _ctznosx
        current_lang.execution_string.split(" "),
        [module],
        [DATASTORE],
        [logging_passthru]
    ))
    
    execution = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout = execution.stdout.readlines()
    stderr = execution.stderr.readlines()

    file_handler = open(log_file, "a")

    for stdout_line in stdout:
        if testing_enabled:
            print log_line(mod_name, stdout_line)

        file_handler.write(log_line(mod_name, stdout_line))

    for stderr_line in stderr:
        if testing_enabled:
            print log_line(mod_name, stderr_line)

        file_handler.write(log_line(mod_name, stderr_line))

# Detect Modules
def launch_modules():
    """launch_modules launches Titan's executable modules"""
    for module in MODULES:
        current_lang = None
        mod_name, ext = splitext(basename(module))

        for language in SUPPORTED_LANGUAGES:
            if ext in language.supported_extensions:
                current_lang = language
                break

        if current_lang is not None and isinstance(current_lang, CtznLanguage):
            if testing_enabled:
                print log_line("ctznOSX", "Found Module: %s/%s, Lang: %s" % (basename(dirname(module)),mod_name, current_lang.execution_string))
            
            spawn_module(module, current_lang, mod_name)

# Default run method
def run():
    # Record Start Time
    start = time()

    # Launch Modules
    launch_modules()

    # Record End Time
    end = time()
    logging.info("Execution took %s seconds.", str(round(end - start, 4)))   

# For Mother Import
if __name__ == "__main__":
    run()
