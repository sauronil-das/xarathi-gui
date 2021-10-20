#!/usr/bin/python

from Tkinter import *
import os
root = Tk()
root.title("ISIS-K")
def Del_btn():
	
	del_lbl=Label(root, text = "Deleted")
	del_lbl.grid(row=1, column =0)
	os.system("./test.py") 


home_lbl = Label(root, text = "WELCOME TO XARATHI")

del_btn = Button(root, text="Click after Reboot", command = Del_btn)



#del_btn = Button(root, text="Click after Reboot", state = DISABLED)

home_lbl.grid(row = 0, column = 0)
del_btn.grid(row=0, column=1)

















root.mainloop()


