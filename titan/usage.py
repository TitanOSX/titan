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

           NxW     NK0xllllox0W      OlN
          0. k  Nd,            .;xW  l .0
         O   .0d.   .,        .   .dO.   0
        K          'dk:      ;:,.        .N
       W,    ;.  ,okkkk,    '::::,   ..   :W
       x    :kx, 'xkkkkd   .:::::;  '::.   x
      X.   ckdlxl.'dkkkk.  '::::,..;:;::.  .N
      l  .okkx'.:xo:lxkk;  ;::;'';;. ':cc'  o
      ;   ,dkko   'lxdkkc  :::::'.   :c:;.  ;
      Nx.   :kkc    ..:kl .::..     ;c;.  'xN
        Wx.  .ok:      od .:'      ;:'  .O
          Wx.  ckxxx.  ,x.':.  .::::. .xW
            o   okk:   .k.,;    ,::'  k
           W,   ,ko    .k;;:    .::   ;W
          Nc    'k,    ckl::.    ,; .  'X    KKKXN
        Wk'  .c.:k;    .,,..     ;:.;;   cdd:   'O
     Wx,.   ckkcxkxc.          .,::;,:,.      ;OW
      WO,  cOkxxkkkkc          ::::::::;.   ;0
        Wk, :kkkkkkkc         .:::::::,   ;0
          WO,.:dkkkkl         .:::::;.  ,0
            Wx, 'okkx.        ':::'.  :0
               O' .lk;        ::'   ,K
                Wd' 'l.      .'   :0
                  Wk, .         ;K
                    Wx.       :K
                      Wx.   ;0
                        N, k

Usage: titanosx [--config=CONFIG] command

%s""" % HELP)

# Unused ATM
#  clean              clean data store contents

MONITOR_USAGE = _("""
Usage: titanosx monitor [ install | list | upgrade | remove ]

commands:
  list               show all installed monitors
  install            installs specified monitor
  upgrade            upgrades specified monitor
  remove             removes specified monitor
""")


MANAGER_USAGE = _("""
Usage: titanosx manager [ register ]

commands:
  register           register this device with a remote server
""")
