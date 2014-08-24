from __future__ import unicode_literals

import argparse
import locale
import sys
from os import listdir,walk,path,environ
from ctznosx import __version__, monitors as Monitors, devicemgmt as Manager
from ctznosx import report as Report
from ctznosx.exceptions import Error
from ctznosx.usage import *
from ctznosx import launcher
from config import ctznConfig

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = path.join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )

def argument_parser(*args, **kwargs):
    format_usage = kwargs.pop('format_usage', None)
    format_help = kwargs.pop('format_help', None)

    class ArgumentParser(argparse.ArgumentParser):

        def format_usage(self):
            return '%s\n' % format_usage

        def format_help(self):
            return '%s\n%s\n' % (self.format_usage(), format_help)

    kwargs['add_help'] = False

    p = ArgumentParser(*args, **kwargs)
    p.add_argument('--help', action='help')
    p.add_argument('-h', action='help')

    return p

# Handles monitor sub-commands
def monitor(args):
    if args is None:
        print MONITOR_USAGE
        sys.exit(1)
    else:
        if args[1] in ('list', 'install', 'remove', 'upgrade'):
            getattr(Monitors, args[1])(args[2:])
        

# Handles monitor sub-commands
def manager(args):
    if args is None:
        print MANAGER_USAGE
        sys.exit(1)        
    else:
        if args[1] in ('register'):
            Manager.register_device()      
        

# Handles clean sub-commands
def clean(args):
    print args

def main(argv=None):
    """
    Handle command line arguments.
    """

    if argv is None:
        argv = sys.argv[1:]
        encoding = locale.getdefaultlocale()[1]
        if encoding:
            argv = [a.decode(encoding) for a in sys.argv[1:]]

    # find command position
    pos, skip_next = 0, False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        else:
            pos = i
            break

    parser = argument_parser(prog='ctznosx', format_usage=USAGE, format_help=HELP)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('-v', action='version', version=__version__)
    parser.add_argument('command')

    try:
        # only parse up until command
        args = parser.parse_args(argv[:pos + 1])
        
        # If this is a plugin install/remove
        if args.command in ('monitor'):
            monitor(argv)

        # If this is a manager based command
        elif args.command in ('manager'):
            manager(argv)

        # Clean subcommand
        elif args.command in ('clean'):
            clean(args)

        # Report subcommand
        elif args.command in ('report'):
            Report.run(argv)

        # Generic Run Script
        else:
            launcher.run()

    except Error as error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)