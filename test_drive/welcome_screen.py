#!/usr/bin/python

from Tkinter import *
import tkMessageBox
import os

'''
import sqlalchemy as db


########################################################################################################################

config = {
         'host': '192.168.122.111',
         'port': 3306,
         'user': 'xaraticli',
         'password': 'SmellyCatSmellyCat',
         'database': 'NIDHI_BANK'
                            }
def connect():
    db_user = config.get('user')
    db_pwd = config.get('password')
    db_host = config.get('host')
    db_port = config.get('port')
    db_name = config.get('database')
    connection_str = "mysql+pymysql://" + db_user + ":" + db_pwd + "@" + db_host + ":" + str(db_port) + "/" + db_name

    engine = db.create_engine(connection_str)

    connection = engine.connect()
    return connection

sql_handle=connect()
'''
###########################################################################################################################

# Button Definations


root = Tk()
root.title("Turin Bank Management Software                  Developed by Sauronil Das")
def reset_after_boot():
	tkMessageBox.showinfo("OPERATOR", "Cache Files Removed From System")
	os.system("") 

def push_rd():
	tkMessageBox.showinfo("OPERATOR", "Data has been pushed to Database")
	os.system("")

def fetch_rd():
	tkMessageBox.showinfo("OPERATOR", "Data has been stored to BALAJI Directory as PCTX.TXT. Please Copy File to Windows Machine")
	os.system("")

def push_loan():
	tkMessageBox.showinfo("OPERATOR", "Data Has been pushed to Database")
	os.system("")

def fetch_loan():
	tkMessageBox.showinfo("OPERATOR", "Data has been stored to BALAJI Directory as PCTX.TXT. Please Copy File to Windows Machine")
	os.system("")

def reconcile_rd():
	tkMessageBox.showinfo("OPERATOR", "Reconciliation of RD Complete")
	os.system("")

def reconcile_loan():
	tkMessageBox.showinfo("OPERATOR", "Reconciliation of LOAN Complete")
	os.system("")

def clear_recon_cache():
	tkMessageBox.showinfo("OPERATOR", "CACHE CLEARED from Database")
	os.system("")

# CSV Function Definations

def super_push():
	tkMessageBox.showinfo("OPERATOR", "Supervisor Has Been Pushed Into Database")
	os.system("")

def agent_push():
	tkMessageBox.showinfo("OPERATOR", "Agent Has Been Pushed Into Database")
	os.system("")
	
def member_push():
	tkMessageBox.showinfo("OPERATOR", "Member Has Been Pushed Into Database")
	os.system("")

def rd_push():
	tkMessageBox.showinfo("OPERATOR", "RD Has Been Pushed Into Database")
	os.system("")
def loan_push():
	tkMessageBox.showinfo("OPERATOR", "LOAN Has Been Pushed Into Database")
	os.system("")

############################################################################################################################

# Button Creation

home_lbl = Label(root, text = "OPERATOR - WELCOME TO XARATHI BANK")
csv_push_lbl = Label(root, text = "Push CSV Data Into Database")
reset_btn = Button(root, text="CLEAR CACHE", command = reset_after_boot)


#############################################################################################################################

# Cronjobs Buttons

push_daily_rd_btn=Button(root, text="Push Daily RD Collection To Database", command=push_rd)
fetch_rd_btn=Button(root, text="Fetch Daily RD for Collection", command=fetch_rd)
push_loan_btn=Button(root, text="Push LOAN Collection to Database", command=push_loan)
fetch_loan_btn=Button(root, text="Fetch LOAN for Collection ", command=fetch_loan)
recon_rd_btn=Button(root, text="Reconcile RD - 4th of Every Month", command=reconcile_rd)
recon_loan_btn=Button(root, text="Reconcile LOAN - 4th of Every Month", command=reconcile_loan)
recon_fix_btn=Button(root, text="Reconcile FIXED DEPOSIT - 4th of Every Month", state= DISABLED)
setup_daily_loan_btn=Button(root, text="Setup Daily Collection for LOAN", state=DISABLED)
clear_recon_cache_btn=Button(root, text="Clear Cache after RECONCILE of RD AND LOAN", command=clear_recon_cache)

#del_btn = Button(root, text="Click after Reboot", state = DISABLED)

# CSV Push Buttons
super_push_btn=Button(root, text="Push Supervisor Info To Database", command=agent_push)
agent_push_btn=Button(root, text="Push Agent Info To Database", command=agent_push)

member_push_btn=Button(root, text="Push Member Info To Database", command=member_push)
rd_push_btn=Button(root, text="Push RD Info To Database", command=rd_push)
loan_push_btn=Button(root, text="Push LOAN Info To Database", command=loan_push)
#############################################################################################################################

# Button Locations

home_lbl.grid(row = 0, column = 0)
reset_btn.grid(row=1, column=0)


push_daily_rd_btn.grid(row=2, column=0)
fetch_rd_btn.grid(row=2, column=1)
push_loan_btn.grid(row=3, column=0)
fetch_loan_btn.grid(row=3, column=1)
recon_rd_btn.grid(row=4, column=0)
recon_loan_btn.grid(row=4, column=1)

recon_fix_btn.grid(row=5, column=0)
setup_daily_loan_btn.grid(row=5, column=1)
clear_recon_cache_btn.grid(row=6, column=0)

csv_push_lbl.grid(row=7, column=0)
super_push_btn.grid(row=8, column=0)
agent_push_btn.grid(row=8, column=1)

member_push_btn.grid(row=9, column=0)
rd_push_btn.grid(row=9, column=1)
loan_push_btn.grid(row=10, column=0)





root.mainloop()


