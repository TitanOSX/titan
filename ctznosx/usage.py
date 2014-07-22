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
  report             display report

""")

# Unused ATM
#  clean              clean data store contents

MONITOR_USAGE = _("""
Usage: ctznosx monitor [ install | list | upgrade | remove ]

commands:
  list               show all installed monitors
  install            installs specified monitor
  upgrade            upgrades specified monitor
  remove             removes specified monitor
""")
