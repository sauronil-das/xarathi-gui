#!/usr/bin/python
import glob
import os
from prettytable import PrettyTable

os.chdir("/home/void/simple_gui/xarathi_gui/BALAJI")

file = glob.glob("*.txt")
myTable = PrettyTable(["Member ID", "Name", "Collection", "Closing Balance", "Date"])

def read_file():

    fp=open(file[0], 'r')
    Lines=fp.readlines()
    data_list=Lines[0].split(',')
    global total_amount
    global date
    total_amount = float(data_list[2].strip(' ').lstrip('0'))
    date = str(data_list[4])
    count = 0
    for line in Lines:
        if "\x1a" in line:
            count+=1
            continue
        if(count>0):
            data_list = line.split(',')
            mem_id = data_list[0].strip(' 0')
            name = data_list[2].strip(' ')
            coll_amt = data_list[1].strip(' ').lstrip('0')
            closing_bal = data_list[3].strip(' ').lstrip('0')
            myTable.add_row([mem_id, name, coll_amt, closing_bal, date])

        count+=1

read_file()

print(myTable)

print "Total Amount = " , total_amount

