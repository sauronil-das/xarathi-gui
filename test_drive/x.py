#!/usr/bin/python

import os

from Tkinter import *

class Application(Frame):
    def say_hi(self):
	var = ".py"
        os.system("./test" + var) #Absolue path for files will be needed

    def createWidgets(self):
        self.CREATE = Button(self)
        self.CREATE["text"] = "Add New Member"
        self.CREATE["fg"]   = "blue"
        self.CREATE["command"] =  self.pack()

        self.CREATE.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
