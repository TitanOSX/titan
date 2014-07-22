from __future__ import unicode_literals

def _(text):
    return text.strip('\n')

USAGE = _("""
Usage: ctznosx [--config=CONFIG] command
""")

HELP = _("""
  -h, --help         show help message
  -v, --version      show version
  --verbose          show script while running
  --dry-run          show script without running

commands:
  run                invoke the scanner
  install            installs specified plugin
  remove             removes specified plugin
  clean              clean data store contents
  report             display report

""")