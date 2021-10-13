#!/usr/bin/python
import calendar
import datetime
from datetime import date, datetime
import sqlalchemy as db
import glob, os
os.chdir("/home/BALAJI/output/rd")
now = datetime.now()
d = now.strftime("%d %B, %Y")
files = glob.glob("*.txt")
config = {
     'host' : '192.168.122.111',
     'port' : 3306,
     'user' : 'xaraticli',
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
sql_handle = connect()
mem_id_paid_list=[]
mem_id_to_collection = {}

global total_collection_day
global total_collection_till_today
global total_rd_collection_till_today

def read_file():
    fp=open(files[0], 'r')
    Lines=fp.readlines()
    data_list=Lines[0].split(',')
    global total_collection_day
    total_collection_day = float(data_list[2].strip(' ').lstrip('0'))
    print total_collection_day
    date=data_list[4].split('.')
    year = now.strftime('%Y')
    global str_day
    str_day = str(year + "-" + date[1] + "-" + date[0])
    count = 0
    for line in Lines:
        if "\x1a" in line:
            count+=1
            continue
        if(count>0):
            data_list = line.split(',')
            mem_id = data_list[0].strip(' ').lstrip('0')
            mem_id_paid_list.append(int(mem_id))
            per_amt_collection = str(data_list[5]).lstrip('0')
            mem_id_to_collection.update({int(mem_id) : float(per_amt_collection) })
        count+=1

read_file()
mem_id_supposed_to_pay_list = []
old_mem_id_to_bal = {}

def getTableInfo(sql_handle):
    sql_string = "SELECT MEMBER_ID, BALANCE from RECCURING_DEPOSITS"
    rs=sql_handle.execute(sql_string)

    for row in rs:
        mem_id_supposed_to_pay_list.append(row[0])
        old_mem_id_to_bal.update({ row[0] : row[1] })

getTableInfo(sql_handle)

def getdefaulterList():
    global defaulter_list
    defaulter_list = list(set(mem_id_supposed_to_pay_list) - set(mem_id_paid_list))

#getdefaulterList()


def updateDefaulterData(sql_handle):
    for defaulter_rd_id in defaulter_list:
        previous_missed_count = old_mem_id_to_pay_miss[defaulter_rd_id]
        new_missed_count = previous_missed_count + 1
        sql_string = "UPDATE RECCURING_DEPOSITS SET PAYMENTS_MISSED = " + str(new_missed_count) + " where MEMBER_ID = " + str(defaulter_rd_id)

        sql_handle.execute (sql_string)

#updateDefaulterData(sql_handle)

def updatePayerData(sql_handle):
    mem_id_paid_list.sort()
    for payer_mem_id in mem_id_paid_list:
        previous_collection_value = old_mem_id_to_bal[payer_mem_id]
        today_collection_value = mem_id_to_collection[payer_mem_id]
        new_collection_value = float(previous_collection_value) + float(today_collection_value)
        sql_string = "UPDATE RECCURING_DEPOSITS SET BALANCE = " + str(new_collection_value) + " where MEMBER_ID = " + str(payer_mem_id)
        sql_handle.execute( sql_string)


updatePayerData(sql_handle)









###########################################################



def update_total_collection(sql_handle):    
    sql_string="INSERT into COLLECTIONS \
                (COLLECTION_DATE, COLLECTION_AMOUNT) values \
                ( \"" + str_day  + "\" ," + str(total_collection_till_today) + " )"
    rs=sql_handle.execute (sql_string)

def get_collections(sql_handle):

    sql_string = "SELECT COLLECTION_AMOUNT from COLLECTIONS WHERE COLLECTION_ID = ( Select Max(COLLECTION_ID) From COLLECTIONS ) " 
    rs = sql_handle.execute (sql_string)

    empty_indicator = True
    for row in rs:
        empty_indicator = False
        amount = row[0]
        old_collection_amt = float(amount)
        global total_collection_till_today
        total_collection_till_today = total_collection_day + old_collection_amt
        update_total_collection(sql_handle)
    if empty_indicator:
        total_collection_till_today = total_collection_day
        update_total_collection(sql_handle)

get_collections(sql_handle)

def update_total_collections_rd(sql_handle):
    sql_string = "INSERT into COLLECTIONS_RD (COLLECTION_DATE, COLLECTION_AMOUNT) VALUES ( \"" + str_day + "\" ," + str(total_rd_collection_till_today) + " )"
    rs=sql_handle.execute (sql_string)

def get_collection_rd(sql_handle):
    sql_string = "SELECT COLLECTION_AMOUNT from COLLECTIONS_RD WHERE COLLECTION_ID = ( Select Max(COLLECTION_ID) From COLLECTIONS_RD )"
    rs=sql_handle.execute (sql_string)
    empty_indicator = True
    for row in rs:
        empty_indicator = False
        amount = row[0]
        old_mem_collection_amt = float(amount)
        global total_rd_collection_till_today
        total_rd_collection_till_today = total_collection_day + old_mem_collection_amt
        update_total_collections_rd(sql_handle)
    if empty_indicator:
        total_rd_collection_till_today = total_collection_day
        update_total_collections_rd(sql_handle)

get_collection_rd(sql_handle)

