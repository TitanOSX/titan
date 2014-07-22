from __future__ import unicode_literals

import argparse
import locale
import os, sys
from ctznosx import __version__, monitors
from ctznosx.exceptions import Error
from ctznosx.usage import *
#from ctznosx import launcher


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
    if args[1] in ('list', 'install', 'remove'):
        getattr(monitors, args[1])(args[2:])
    else:
        print MONITOR_USAGE
        sys.exit(1)

# Handles clean sub-commands
def clean(args):
    print args

def report(args):
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

        elif args.command in ('clean'):
            clean(args)

        elif args.command in ('report'):
            report(args)

        # Generic Run Script
        else:
            pass
            #launcher(args).run(args.command, argv[pos + 1:])

    except Error as error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)