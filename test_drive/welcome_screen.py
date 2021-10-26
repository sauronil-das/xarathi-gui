#!/usr/bin/python

from Tkinter import *
import tkSimpleDialog as simpledialog
import tkMessageBox
import os

###########################################################################################################################

# Button Definations


root = Tk()
root.title("Turin Bank Management Software                  Developed by Sauronil Das")
root.geometry("1000x600")

#############################################################################################################################

# Entry Definnations



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


def list_all_rd():
	tkMessageBox.showinfo("OPERATOR", "RD Data has been Copied to Directory. Please Check")
	os.system("")

def list_all_loans():
	tkMessageBox.showinfo("OPERATOR", "LOAN Data has been Copied to Directory. Please Check")
	os.system("")

def list_all_members():
	tkMessageBox.showinfo("OPERATOR", "Members Data has been Copied to Directory. Please Check")
	os.system("")

def list_all_super():
	tkMessageBox.showinfo("OPERATOR", "Supervisor Data has been Copied to Directory. Please Check")
	os.system("")

def list_mem_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system(" ")	

def list_rd_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system(" ")	

def list_loan_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system(" ")	

############################################################################################################################

# Button Creation

home_lbl = Label(root, text = "OPERATOR - WELCOME TO XARATHI BANK", fg='blue', font=("Helvetica", 24, 'bold'))
csv_push_lbl = Label(root, text = "||Push CSV Data Into Database||", fg='blue', font=("Courier", 18))
reset_btn = Button(root, text="CLEAR CACHE", fg='red', command = reset_after_boot)
list_lbl = Label(root, text="||All Listing Commands||", fg='blue', font=("Courier", 18))

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
clear_recon_cache_btn=Button(root, text="Clear Cache after RECONCILE of RD AND LOAN", fg='red', command=clear_recon_cache)

#del_btn = Button(root, text="Click after Reboot", state = DISABLED)

# CSV Push Buttons
super_push_btn=Button(root, text="Push Supervisor Info To Database", command=agent_push)
agent_push_btn=Button(root, text="Push Agent Info To Database", command=agent_push)

member_push_btn=Button(root, text="Push Member Info To Database", command=member_push)
rd_push_btn=Button(root, text="Push RD Info To Database", command=rd_push)
loan_push_btn=Button(root, text="Push LOAN Info To Database", command=loan_push)


# Operator List Buttons (Display and Output)

list_all_rd_btn=Button(root, text="Print All Reccuring Desposits", command=list_all_rd)
list_all_loans_btn=Button(root, text="Print All Loans", command=list_all_loans)
list_all_members_btn=Button(root, text="Print All Members", command=list_all_members)
list_all_super_btn=Button(root, text="Print All Members", command=list_all_super)
list_mem_with_id_btn=Button(root, text="Print Member with Specific ID", command=list_mem_with_id)
list_rd_with_id_btn=Button(root, text="Print Reccuring with Specific Member ID", command=list_rd_with_id)
list_loan_with_id_btn=Button(root, text="Print LOANS with Specific Member ID", command=list_loan_with_id)
#############################################################################################################################

# Button Locations

home_lbl.grid(row = 0, column = 0)
reset_btn.grid(row=1, column=0, sticky=W)


push_daily_rd_btn.grid(row=2, column=0, sticky=W)
fetch_rd_btn.grid(row=2, column=1, sticky=E)
push_loan_btn.grid(row=3, column=0, sticky=W)
fetch_loan_btn.grid(row=3, column=1, sticky=E)
recon_rd_btn.grid(row=4, column=0, sticky=W)
recon_loan_btn.grid(row=4, column=1, sticky=E)

recon_fix_btn.grid(row=5, column=0, sticky=W)
setup_daily_loan_btn.grid(row=5, column=1, sticky=E)
clear_recon_cache_btn.grid(row=6, column=0, sticky=W)

csv_push_lbl.grid(row=7, column=0, sticky=W)

super_push_btn.grid(row=8, column=0, sticky=W)
agent_push_btn.grid(row=8, column=1, sticky=E)
member_push_btn.grid(row=9, column=0, sticky=W)
rd_push_btn.grid(row=9, column=1, sticky=E)
loan_push_btn.grid(row=10, column=0, sticky=W)

list_lbl.grid(row=11, column=0, sticky=W)

list_all_rd_btn.grid(row=12, column=0, sticky=W)
list_all_loans_btn.grid(row=12, column=1, sticky=E)
list_all_members_btn.grid(row=13, column=0, sticky=W)
list_all_super_btn.grid(row=13, column=1, sticky=E)
list_mem_with_id_btn.grid(row=14, column=0, sticky=W)
list_rd_with_id_btn.grid(row=14, column=1, sticky=E)
list_loan_with_id_btn.grid(row=15, column=0, sticky=W)




root.mainloop()


