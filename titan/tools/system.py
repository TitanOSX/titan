#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
import plistlib
from re import IGNORECASE
from re import compile as recompile
from os.path import isfile, split

def hw_details():
    details = {}
    output = execute_command("system_profiler SPHardwareDataType")

    details["serial_number"] = parse_output( 'Serial', output )
    details["hardware_uuid"] = parse_output( 'UUID', output )
    details["machine_name"] = parse_output( 'Model Identifier', output )
    details["machine_model"] = parse_output( 'Model Name', output )
    details["machine_make"] = "Apple"
    details["cpu_type"] = parse_output( 'Processor Name', output )
    details["cpu_speed"] = parse_output( 'Processor Speed', output )
    details["physical_memory"] = parse_output( 'Memory', output )
    details['model_short'] = details["serial_number"][-4:]

    return details

def sw_details():
    details = {}
    output = execute_command("sw_vers")
    
    details["os_version"] = parse_output("ProductVersion", output)
    details["os_build"] = parse_output("BuildVersion", output)

    return details

# Retruns Mac Serial Number
def hw_serial():
    return execute_command("ioreg -c IOPlatformExpertDevice |head -30 |grep IOPlatformSerialNumber | awk '{print $4}'")[1:-2]

# Alias to execute_command
def shell_out( command ):
    return execute_command( command )
    
# Executes a system command
def execute_command( command ):
 	ps = Popen(command,shell=True,stdout=PIPE,stderr=STDOUT)
 	output = ps.communicate()[0]
 	return output

def parse_output( find_this, in_this ):
    for line in in_this.splitlines():
        if find_this.lower() in line.lower():
            return line.split(':')[-1].strip()

def get_kextstat():
    """
    Returns a nice JSON array of `kextstat`
    """
    kextstat = shell_out("kextstat -l")
    header = [
        'Index',
        'Refs',
        'Address',
        'Size',
        'Wired',
        'Name',
        'Version',
        'Linked Against'
    ]
    kextstat_json = {}
    for i in range(len(kextstat)):
        mod = filter(None, kextstat[i].split(" "))
        mod = mod[:7] + ["-".join(mod[7:])]
        kextstat[i] = mod

    for i in kextstat:
        j = dict(zip(header, i))
        kextstat_json[j["Index"]] = j

    return kextstat_json


def get_kextfind():
    """
    Returns an array of .kext files
    """
    kextfind = shell_out("kextfind")
    if kextfind:
        return kextfind
    else:
        return None


def get_launchctl():
    """
    Returns a nice JSON array of `launchctl list`
    """
    launchctl = shell_out("/bin/launchctl list")
    header = ["PID", "Status", "Label"]
    launchctl_json = {}

    launchctl = launchctl[1::]

    for i in range(len(launchctl)):
        mod = filter(None, launchctl[i].split("\t"))
        launchctl[i] = mod

    for i in range(len(launchctl)):
        j = dict(zip(header, launchctl[i]))
        launchctl_json[i] = j

    return launchctl_json


def strings(executable):
    """
    Returns an array of unique strings found in a supplied executable
    """
    if isfile(executable):
        try:
            strings_list = list(set(shell_out("strings %s" % executable)))
        except OSError:
            return []
        except Exception:
            return []
        if strings_list:
            return strings_list
        else:
            return []
    else:
        return []


def delete_file(filename):
    """
    Calls "rm" on a supplied file
    """
    call(["rm", "-f", filename])


def installed(program):
    """
    Returns the path of a supplied program if the supplied program is installed
    and returns False if it is not
    """
    which = shell_out("mdfind -name %s" % program)
    if which:
        for i in which:
            _, fname = split(i)
            if fname == program:
                return i
    else:
        return False


def last_user_name():
    """
    Returns the last logged in username from com.apple.loginwindow.plist
    """
    command = " ".join([
        "defaults",
        "read",
        "/Library/Preferences/com.apple.loginwindow.plist",
        "lastUserName",
    ])
    last_user = shell_out(command)
    if len(last_user) != 1:
        return False
    else:
        last_user = last_user[0]
    return last_user


def crontab_for_user(user):
    """
    Returns False is a supplied user doesn't have a crontab, and returns the
    crontab (pipes in place of newlines) if the user does have one
    """
    crontab = filter(None, shell_out("crontab -u %s -l" % user))
    if crontab:
        return '|'.join(crontab)
    else:
        return False


def last():
    """
    Returns the first two columns of the `last` command
    """
    last_command = shell_out("last")[:-2]
    last_output = []
    for i in last_command:
        last_output.append(filter(None, i.split(" "))[:2])
    return last_output


def list_users():
    """
    Returns an array of all 'users' on the system
    """
    users = []
    dscacheutil = shell_out("dscacheutil -q user")
    if dscacheutil:
        for i in dscacheutil:
            if i.startswith('name: '):
                users.append(i[6:])
    return users


def run_file(filename):
    """
    Returns file information on a given filename. Returns None if file doesn't
    exist
    """
    if isfile(filename):
        output = shell_out("file %s" % filename)
        if output:
            try:
                output = output[0]
            except OSError:
                return None
            except:
                return None
            if output:
                return output
        return None


def lsof():
    """
    Returns a array of lsof -i data
    """
    lsof_output = shell_out("lsof -i")
    lsof_data = []
    headers = [
        'command',
        'pid',
        'user',
        'fd',
        'type',
        'device',
        'size/off',
        'node',
        'name',
    ]
    lsof_output = lsof_output[1:]

    for i in lsof_output:
        lsof_data.append(dict(zip(headers, filter(None, i.split(" ")))))

    return lsof_data


def is_fde_enabled():
    """
    Returns True if FDE is enabled, False if it is not
    """
    fde = shell_out("fdesetup status")
    if fde == ['FileVault is On.']:
        return True
    return False