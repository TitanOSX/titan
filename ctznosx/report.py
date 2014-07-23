import tempfile
import commands
from time import sleep
from os import listdir,walk,path,environ,unlink
from config import TiConfig as ctznConfig
from titantools.orm import TiORM as ctznORM

# Get ctznOSX Env and Config
CTZNOSX_PATH = (environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/')
CTZNOSX_CONFIG = path.join('/etc/', 'ctznosx.conf')

# Config
CONFIG = ctznConfig( CTZNOSX_CONFIG, CTZNOSX_PATH )
DATASTORE = CONFIG['main']['datastore']

def header():
    text = """
<html>
<head>
    <title>ctznOSX - Report</title>
    <style>
    body {
        font-family: "Menlo", sans;
    }

    .block {
        width: 100%;
        margin:10px 0px 25px 0px;
    }
    
    table {
        width: 100%;
        margin-bottom: 16px;
    }

    tr:nth-child(even) {background: #efefef;}
    tr:nth-child(odd) {background: #fff;}
    
    </style>
    <script>

    </script>
</head>
<body>
    """
    return text.replace(chr(0xa0), ' ')

def footer():
    text = """
</body>
</html>    
    """
    return text
    
# Run Report
def run():
    report = header()

    # Load ORM 
    ORM = ctznORM(DATASTORE)

    # Get all tables
    all_monitors = ORM.select('sqlite_master', 'name',  "type = 'table' and name != 'watcher'")
    for monitor in all_monitors:
        report += "<div class=\"block\">"
        report += "<h2>%s</h2>\n" % monitor['name']
        module_data = ORM.select( monitor['name'], '*' )
        
        for row in module_data:
            report += "<table>\n"
            for column in row:
                if "_" not in column:
                    report += "\t<tr>\n"
                    report += "\t\t<td>\n"
                    report += column
                    report += "\t\t</td>\n"

                    report += "\t\t<td>\n"
                    report += str(row[str(column)]).replace("\n", "<br/>\n")
                    report += "\t\t</td>\n"
                    report += "\t</tr>\n"
            report += "</table>\n"

        report += "</div>"

    report += footer()

    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(report)
    f.close() # file is not immediately deleted because we
              # used delete=False

    res = commands.getoutput("open %s" % (f.name))
    sleep(10)
    unlink(f.name)