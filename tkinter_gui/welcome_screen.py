#!/usr/bin/python

from Tkinter import *
import tkSimpleDialog as simpledialog
import tkMessageBox
import os

##########################################################################################

# Button Definations


root = Tk()
root.title("Turin Bank Management Software                  Developed by Sauronil Das")
root.geometry("1000x600")

###########################################################################################
# Entry Definnations



def reset_after_boot():
	tkMessageBox.showinfo("OPERATOR", "Cache Files Removed From System")
	os.system("rm -r /home/BALAJI/output/rd/*") 
	os.system("rm -r /home/BALAJI/output/loans/*") 
	os.system("rm -r /home/BALAJI/input/rd/*") 
	os.system("rm -r /home/BALAJI/input/loans/*") 


def push_rd():
	tkMessageBox.showinfo("OPERATOR", "Data has been pushed to Database")
	os.system("/home/cronjobs/push_daily_rd_collection_to_db.py")

def fetch_rd():
	tkMessageBox.showinfo("OPERATOR", "Data has been stored to BALAJI Directory as PCTX.TXT. Please Copy File to Windows Machine")
	os.system("/home/cronjobs/fetch_rd_for_collection.py")

def push_loan():
	tkMessageBox.showinfo("OPERATOR", "Data Has been pushed to Database")
	os.system("/home/cronjobs/push_daily_loan_collection_to_db.py")

def fetch_loan():
	tkMessageBox.showinfo("OPERATOR", "Data has been stored to BALAJI Directory as PCTX.TXT. Please Copy File to Windows Machine")
	os.system("/home/cronjobs/fetch_loans_for_collection.py")

def reconcile_rd():
	tkMessageBox.showinfo("OPERATOR", "Reconciliation of RD Complete")
	os.system("/home/cronjobs/reconcile_rd_payments.py")

def reconcile_loan():
	tkMessageBox.showinfo("OPERATOR", "Reconciliation of LOAN Complete")
	os.system("/home/cronjobs/reconcile_loan_payments.py")

def clear_recon_cache():
	tkMessageBox.showinfo("OPERATOR", "CACHE CLEARED from Database")
	os.system("/home/cronjobs/delete_month_payment_after_reconcile.py")

# CSV Function Definations

def super_push():
	tkMessageBox.showinfo("OPERATOR", "Supervisor Has Been Pushed Into Database")
	os.system("/home/sauronil/pusher_scripts/supervisor_pusher.py")

def agent_push():
	tkMessageBox.showinfo("OPERATOR", "Agent Has Been Pushed Into Database")
	os.system("/home/sauronil/pusher_scripts/agent_pusher.py")
	
def member_push():
	tkMessageBox.showinfo("OPERATOR", "Member Has Been Pushed Into Database")
	os.system("/home/sauronil/pusher_scripts/members_pusher.py")

def rd_push():
	tkMessageBox.showinfo("OPERATOR", "RD Has Been Pushed Into Database")
	os.system("/home/sauronil/pusher_scripts/rd_pusher.py")
def loan_push():
	tkMessageBox.showinfo("OPERATOR", "LOAN Has Been Pushed Into Database")
	os.system("/home/sauronil/pusher_scripts/loan_pusher.py")


def list_all_rd():
	tkMessageBox.showinfo("OPERATOR", "RD Data has been Copied to Directory. Please Check")
	os.system("/home/sauronil/operator_scripts/list_all_rd.py > /home/sauronil/Desktop/operation_files/all_rd.txt")

def list_all_loans():
	tkMessageBox.showinfo("OPERATOR", "LOAN Data has been Copied to Directory. Please Check")
	os.system("/home/sauronil/operator_scripts/list_all_loans.py > /home/sauronil/Desktop/operation_files/all_loans.txt")

def list_all_members():
	tkMessageBox.showinfo("OPERATOR", "Members Data has been Copied to Directory. Please Check")
	os.system("/home/sauronil/operator_scripts/list_all_members.py > /home/sauronil/Desktop/operation_files/all_members.txt")

def list_all_super():
	tkMessageBox.showinfo("OPERATOR", "Supervisor Data has been Copied to Directory. Please Check")
	os.system("/home/sauronil/operator_scripts/list_super.py > /home/sauronil/Desktop/operation_files/all_supervisors.txt")

def list_mem_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system("/home/sauronil/operator_scripts/list_member_with_id.py " + str(mem_id) + " > /home/sauronil/Desktop/operation_files/member.txt")	

def list_rd_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system("/home/sauronil/operator_scripts/list_rd_with_id.py " + str(mem_id) + " > /home/sauronil/Desktop/operation_files/rd.txt")	

def list_loan_with_id():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	os.system("/home/sauronil/operator_scripts/list_loan_with_id.py " + str(mem_id) + " > /home/sauronil/Desktop/operation_files/loan.txt")	
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
list_all_super_btn=Button(root, text="Print All Supervisors", command=list_all_super)
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


