#!/usr/bin/env python
# coding: utf-8
import sys, os
import syslog
import commands
import datetime
import time
import requests
#import logging
#import logging.handlers
#from logger import create_logger
#import logger
import subprocess
from prettytable import PrettyTable
import readline
import getpass

from sql_connect import connect
from sql_connect import fetch_person_entries
from sql_connect import fetch_address_by_id
from sql_connect import fetch_account_by_member
from sql_connect import fetch_collection_by_account_id
from sql_connect import fetch_agents_by_supervisor
from sql_connect import fetch_members_by_agent
from sql_connect import fetch_agent_by_member
from sql_connect import fetch_super_by_member


HELP = """
help                                               : Display help
display                                            : Display all configuration
clear                                              : Clear screen
connect                                            : Connect to Database
show <supers|agents|members>                       : List all Supervisors Agents and Members
show_addr <supers|agents|members><id>              : Display address of Supervisors Agents and Members
list <loans|fds|rds|stocks><memberid>              : List Loans Fixed Deposits Recurring Deposits and Stocks by Member ID
super_agent_list <superid>                         : List all agents under a Supervisor
agent_member_list <superid>                        : List all members under an Agent
get_agent <member_id>                              : Get Agent Detail serving a Member
get_super <member_id>                              : Get Supervisor Detail serving a Member
show_collection <loans|rds><id>                    : Get current month collection data by loan or rd if
exit                                               : Exit from current prompt
"""

COMMANDS = ['help', 'display', 'clear', 'connect', 'show', 'show_addr', 'list', 'super_agent_list',
            'agent_member_list', 'get_agent', 'get_super', 'show_collection', 'exit']

#########################################################################################################
#                                               Global Variable Section                                 #
#########################################################################################################
current_dir                       = os.path.dirname(os.path.realpath(__file__))
log_file                          = "%s/logs/deploy_manager.log" %current_dir

#########################Utilities#####################################################################
def runner(command):
    p = subprocess.Popen([ command ], shell = True, stdout = subprocess.PIPE)
    output = p.stdout.read()
    p.terminate()
    return output.rstrip('\r\n')

def runWithReturnCode(command):
    try:
        retcode = subprocess.call([ command ], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        #retcode = subprocess.call([ command ], shell = True)
        if retcode == 0:
            return True
        else:
            return False
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
        return False

def isInt(var):
    try: 
        int(var)
        return True
    except ValueError:
        return False

def cmdLogger(command):
    user = runner('whoami')
    temppass = ""
    noprint = False
    logcmd = ""
    logcmd = datetime.datetime.now().strftime("%b  %d %Y %H:%M:%S")
    logcmd = logcmd + " " + user + ":"
    if "add-user" == command[0]:
        noprint = True
    if noprint and len(command) >= 3:
        temppass = command[2]
        command[2] = "******"

    if "add-sftp-host" == command[0]:
        noprint = True
    if noprint and len(command) >= 5:
        temppass = command[4]
        command[4] = "*******"

    for cmd in command:
        logcmd = logcmd + " " + str(cmd)
    logcmd = logcmd + " \n"
    commandLogF.write(logcmd)
    if noprint:
        if command[0] == "add-user" and len(command) >= 3:
            command[2] = temppass
        if command[0] == "add-sftp-host" and len(command) >= 5:
            command[4] = temppass

runner("touch /home/CLI-LOGS/nidhi-bank-history")
commandLogF = open("/home/CLI-LOGS/nidhi-bank-history", "a", buffering=1)

def completer(text, state):
    options = [x for x in COMMANDS if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None
readline.set_completer(completer)
readline.parse_and_bind("tab:complete")

class bcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

#########################CLI_COMMAND_Functions################################################################
def list_entries(entry_type, connection):
    rs = fetch_person_entries(entry_type, connection)
    if entry_type == 'supers':
        x = PrettyTable()
        x.field_names = ["SUPER_ID", "FIRST_NAME", "LAST_NAME", "BIRTH_DATE", "JOINING_DATE", "TERMINATION_DATE" ]
        for row in rs:
            x.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
        print (x)
    elif entry_type == 'agents':
        x = PrettyTable()
        x.field_names = ["AGENT_ID", "SUPERVISOR_ID", "FIRST_NAME", "LAST_NAME", "BIRTH_DATE", "JOINING_DATE", "TERMINATION_DATE"]
        for row in rs:
            x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        print (x)
    elif entry_type == 'members':
        x = PrettyTable()
        x.field_names = ["MEMBER_ID", "AGENT_ID", "FIRST_NAME", "LAST_NAME", "BIRTH_DATE", "MEMBERSHIP_DATE", "TERMINATION_DATE"]
        for row in rs:
            x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        print (x)
    return

def list_account_details(account_type, member_id, connection):
    rs = fetch_account_by_member(account_type, member_id, connection)
    x = PrettyTable()
    x.field_names = ["ID", "NAME", "OPEN_DATE", "AIR", "PRINCIPAL", "DURATION", "PRI_BAL", "PROC_FEE", "PMT_MADE", "PMT_MISS", "STATUS", "EMI", "PENALTY", "REMARKS", "SUP_ID", "AGENT_ID"]
    for row in rs:
        x.add_row(row)
    print (x)
    return

def list_collection_details( account_type, account_id, connection):
    rs = fetch_collection_by_account_id(account_type, account_id, connection)
    x = PrettyTable()
    x.field_names = [ "ID", "COLLECT_MONTH_YEAR", "COLLECTION_COUNT", "COLLECTION_MISSED",
                      "COLLECTION_PER_DAY", "COLLECTION_AMOUNT", "TOTAL_DAYS" ]
    for row in rs:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    print (x)
    return

def show_address(person_type, person_id, connection):
    rs = fetch_address_by_id(person_type, person_id, connection)
    x = PrettyTable()
    x.field_names = ["ID", "CURRENT_ADDRESS", "PERMANENT_ADDRESS"]
    for row in rs:
        x.add_row([row[0], row[1], row[2]])
    print (x)
    return

def list_agents_by_supervisor(supervisor_id, connection):
    rs = fetch_agents_by_supervisor(supervisor_id, connection) 
    x = PrettyTable()
    x.field_names = ["AGENT_ID", "SUPER_ID", "FIRST_NAME", "LAST_NAME", "JOIN_DATE", "PERMA_ADDR" ]
    for row in rs:
        x.add_row(row)
    print(x)
    return
def list_members_by_agent(agent_id, connection):
    rs = fetch_members_by_agent(agent_id, connection)
    x = PrettyTable()
    x.field_names = ["MEM_ID", "AGENT_ID", "FIRST_NAME", "LAST_NAME", "JOIN_DATE", "NUM_STK", "STK_VAL", "PERMA_ADDR", "CURR_ADDR" ]
    for row in rs:
        x.add_row(row)
    print(x)
def get_agent_of_member(member_id, connection):
    fetch_agent_by_member(member_id, connection)
    return
def get_super_of_member(member_id, connection):
    fetch_super_by_member(member_id, connection)
    return
def print_help():
    table = PrettyTable(['Command', 'Options', 'Purpose'])
    all_help = HELP.split("\n")
    for command in all_help:
        Options = None
        if command == "" or command == " " or command == '' or command == ' ':
            continue
        Purpose = command.split(":")[1]
        cmd_split = command.split(":")[0]
        cmd_split = cmd_split.rstrip()
        if len(cmd_split.split(" ")) >= 2:
            Options = cmd_split.split(" ")[-1].rstrip()
            Options = cmd_split.split(" ")[-1].lstrip()
            cmd_split = cmd_split.split(" ")[0].rstrip()
        table.add_row([cmd_split,Options,command.split(":")[1]])
    table.align = "l"
    print table

def main():
    connection = None
    me = runner("whoami")
    #orchastrator_obj = saegw_orchastrator()
    cmd = 'clear'
    p = subprocess.Popen([ cmd ], shell = True, stdout = subprocess.PIPE)
    output = p.stdout.read()
    print output
    p.terminate()
    print "************************ NidhiBank Data Manager *************************"
    print "*                        When in doubt run help                         *"
    print "*************************************************************************"
    while True:
        commandPresent = False
        cmd = raw_input('NidhiBank-Data-Manager(' + me + ')> ')
        cmd = cmd.rstrip(" ")
        cmd = cmd.split(" ")
        cmd_count = len(cmd)
        if cmd_count <= 5:
            if not cmd[0] == '' and cmd_count == 3:
                full_command = cmd[0] + ' ' + cmd[1]
            else:
                full_command = cmd
            for i in range(cmd_count):
                if cmd[i] == 'help':
                    #print HELP
                    cmdLogger(cmd)
                    print_help()
                    commandPresent = True
                    continue
                if cmd[i] == 'clear':
                    cmdLogger(cmd)
                    commandPresent = True
                    os.system("clear")
                    continue
                if cmd[i] == 'connect':
                    cmdLogger(cmd)
                    commandPresent = True
                    connection = connect()
                    continue
                if cmd[i] == 'show':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif cmd_count == 2 and (cmd[i+1]=='supers' or cmd[i+1]=='agents' or cmd[i+1]=='members' ):
                        list_entries(cmd[i+1], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue
                if cmd[i] == 'show_addr':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif (
                            cmd_count == 3  and
                            (cmd[i+1]=='supers' or cmd[i+1]=='agents' or cmd[i+1]=='members') and
                            ( isInt(cmd[i+2]))):
                        show_address( cmd[i+1], cmd[i+2], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue
                if cmd[i] == 'list':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif (
                            cmd_count == 3  and
                            (cmd[i+1]=='loans' or cmd[i+1]=='fds' or cmd[i+1]=='rds' or cmd[i+1]=='stocks') and
                            ( isInt(cmd[i+2]))):
                        list_account_details( cmd[i+1], cmd[i+2], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue

                if cmd[i] == 'show_collection':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif (
                            cmd_count == 3  and
                            (cmd[i+1]=='loans' or cmd[i+1]=='rds') and
                            ( isInt(cmd[i+2]))):
                        list_collection_details( cmd[i+1], cmd[i+2], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue
 
                if cmd[i] == 'super_agent_list':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif cmd_count == 2 and isInt(cmd[i+1]):
                        list_agents_by_supervisor(cmd[i+1], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue

                if cmd[i] == 'agent_member_list':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif cmd_count == 2 and isInt(cmd[i+1]):
                        list_members_by_agent(cmd[i+1], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue

                if cmd[i] == 'get_agent':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif cmd_count == 2 and isInt(cmd[i+1]):
                        get_agent_of_member(cmd[i+1], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue
 
                if cmd[i] == 'get_super':
                    cmdLogger(cmd)
                    commandPresent = True
                    if (connection is None):
                        print "Please run connect to connect to DB first"
                        continue
                    elif cmd_count == 2 and isInt(cmd[i+1]):
                        get_super_of_member(cmd[i+1], connection)
                        continue
                    else:
                        print "Please use help to use the correct command syntax"
                        continue

                elif cmd[i] == 'exit' or cmd[i] == 'end' or cmd[i] == 'quit':
                    cmdLogger(cmd)
                    print 'Exiting . . . . . '
                    os._exit(0)
                elif commandPresent != True:
                    if cmd[0] == "":
                        continue
                    #logger.error("Command %s entered not supported" %cmd[0])
                    #logger.info("Enter [help] to see list of commands")
                    print HELP
                    break
                    #continue
        else:
            print "More than four Arguments NOT accepted."

if __name__ == '__main__':
    #os.system("mkdir -p /home/CLI-LOGS/logs/")
    #os.system("mkdir -p /home/CLI-LOGS/tmp/")
    #logger            = create_logger("xarati_cli",log_file,logging.DEBUG)
    #logger            = logging.getLogger("xarati_cli",log_file,logging.DEBUG)
    #if logger == None:
    #    print "ERROR:Failed to capture deploy_manager logs..Exiting"
    #    sys.exit(1)
    #else:
    #    logger.propagate    = False
    try:
        main()
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        #traceback.print_exc()
        os._exit(1)
