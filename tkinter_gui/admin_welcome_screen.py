#!/usr/bin/python

from Tkinter import *
import tkSimpleDialog as simpledialog
import tkMessageBox
import os


root = Tk()
root.title("Turin Bank Management Software                  Developed by Sauronil Das")
root.geometry("900x600")


# Button Definations

def delete_agent():
	agent_id=simpledialog.askstring("Input", "Enter AGENT ID")
	print agent_id
	os.system("")

def delete_loan():
	loan_id=simpledialog.askstring("Input", "Enter LOAN ID")
	print loan_id
	os.system("")


def delete_member():
	mem_id=simpledialog.askstring("Input", "Enter MEMBER ID")
	print mem_id
	os.system("")


def delete_rd():
	rd_id=simpledialog.askstring("Input", "Enter RD ID")
	print rd_id
	os.system("")

def set_penalty():
	penalty=simpledialog.askstring("Input", "Enter Penalty Amount")
	loan_id=simpledialog.askstring("Input", "Enter LOAN ID")
	os.system("")

def update_rd_balance():
	balance=simpledialog.askstring("Input", "Enter Balance Amount")
	rd_id=simpledialog.askstring("Input", "Enter RD ID")
	print balance
	print rd_id
# Button Creation

home_lbl = Label(root, text = "ADMIN - WELCOME TO XARATHI BANK")
warning_lbl = Label(root, text="|| CAREFULL WHEN USING ||", fg='red', font=("Courier", 28))
#############################################################################################################################


delete_agent_btn=Button(root, text="Delete AGENT", command=delete_agent)
delete_loan_btn=Button(root, text="Delete LOAN", command=delete_loan)
delete_member_btn=Button(root, text="Delete MEMBER", command=delete_member)
delete_rd_btn=Button(root, text="Delete RECCURING DEPOSIT", command=delete_rd)
set_penalty_on_loan_btn=Button(root, text="Set PENALTY on LOAN", command=set_penalty)
update_balance_btn=Button(root, text="Update RD Balance", command=update_rd_balance)

close_btn=Button(root, text="Exit", command=root.destroy)

# Button Grid Locations
warning_lbl.grid(row=0, column=0, sticky=W)
delete_agent_btn.grid(row=1, column=0, sticky=W)
delete_loan_btn.grid(row=1, column=1, sticky=E)
delete_member_btn.grid(row=2, column=0, sticky=W)
delete_rd_btn.grid(row=2, column=1, sticky=E)

set_penalty_on_loan_btn.grid(row=3, column=0, sticky=W)

update_balance_btn.grid(row=3, column=1, sticky=E)
close_btn.grid(row=4, column=0, sticky=W)
root.mainloop()


