from __future__ import unicode_literals

def _(text):
    return text.strip('\n')

HELP = _("""
  -h, --help         show help message
  -v, --version      show version
  --verbose          show script while running
  --dry-run          show script without running

commands:
  run                invoke the scanner
  device             manage device
  monitor            manage monitors
  report             display report

""")

USAGE = _("""
                                  MMP\"""\""YMM MP\"""\"""`MM M""MMMM""M
           dP                     M' .mmm. `M M  mmmmm..M M  `MM'  M
           88                     M  MMMMM  M M.      `YM MM.    .MM
.d8888b. d8888P d888888b 88d888b. M  MMMMM  M MMMMMMM.  M M  .mm.  M
88'  `""   88      .d8P' 88'  `88 M. `MMM' .M M. .MMM'  M M  MMMM  M
88.  ...   88    .Y8P    88    88 MMb     dMM Mb.     .dM M  MMMM  M
`88888P'   dP   d888888P dP    dP MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMM

Usage: ctznosx [--config=CONFIG] command

%s""" % HELP)

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


MANAGER_USAGE = _("""
Usage: ctznosx manager [ register ]

commands:
  register           register this device with a remote server
""")
