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
  monitor            manage monitors
  clean              clean data store contents
  report             display report

""")

MONITOR_USAGE = _("""
Usage: ctznosx monitor [ install | list | remove ]

commands:
  list               show all installed monitors
  install            installs specified monitor
  remove             removes specified monitor
""")
