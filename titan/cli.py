from __future__ import unicode_literals

import argparse
import locale
import sys
from os.path import join
from os import listdir,walk,path,environ
from titan import __version__, monitors as Monitors, devicemgmt as Manager
from titan import report as Report
from titan.exceptions import Error
from titan.usage import *
from titan import launcher
from config import titanConfig

# Get titanOSX Env and Config
TITAN_PATH = (environ.get('TITAN_PATH') or '/var/lib/titan/')
TITAN_CONFIG = join('/etc/', 'titan.conf')

# Config
CONFIG = titanConfig( TITAN_CONFIG, TITAN_PATH )

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
        else:
            print MONITOR_USAGE
            sys.exit(1)

# Handles monitor sub-commands
def manager(args):
    if args is None:
        print MANAGER_USAGE
        sys.exit(1)        
    else:
        if args[1] in ('register', 'unregister', 'status'):
            getattr(Manager, args[1])(args[2:])
        else:
            print MANAGER_USAGE
            sys.exit(1)

# Handles clean sub-commands
def clean(args):
    pass
    #print args

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

    parser = argument_parser(prog='titanosx', format_usage=USAGE, format_help=HELP)
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
        elif args.command in ('run'):
            launcher.run()
        else:
            print USAGE
            sys.exit(1)

    except Error as error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
