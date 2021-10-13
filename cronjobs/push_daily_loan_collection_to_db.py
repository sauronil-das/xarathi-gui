#!/usr/bin/python
import calendar
import datetime
import sqlalchemy as db

import glob, os
os.chdir("/home/BALAJI/output/loans")


files = glob.glob("*.csv")
d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")
config = {
    'host' : '192.168.122.111'
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

loan_id_paid_list = []
loan_id_to_collection_dict = {}

def read_file(sql_handle):

    fp=open(files[0], 'r')
    Lines=fp.readlines()

#special case from line 0, where we only need to fetch total collection for the day
    data_list=Lines[0].split(',')
    global total_collection_day
    total_collection_day = float(data_list[2].strip(' ').lstrip('0'))
    date=data_list[4].split('.')
    year = now.strftime('%Y')
    global str_day
    str_day =  str(year + "-" + date[1] + "-" + date[0])

    count = 0
    for line in Lines:
        if "\x1a" in line:
            count+=1
            continue
        if(count>0) :
            data_list = line.split(',')
            loan_id = data_list[0].strip(' ').lstrip('0')
            loan_id_paid_list.append(int(loan_id))
            per_amt_collection = str(data_list[5]).replace('\r', '').replace(' ', '').rstrip('\n').lstrip('0')
            loan_id_to_collection_dict.update( { int(loan_id) : float(per_amt_collection) } )
        count+=1

read_file(sql_handle)


loan_id_supposed_to_pay_list = []
old_loan_id_to_coll_succ = {}
old_loan_id_to_coll_miss = {}
old_loan_id_to_coll_amnt = {}

def getTableInfo(sql_handle):
    sql_string = "SELECT LOAN_ID, COLLECTION_COUNT, COLLECTION_MISSED, COLLECTION_AMOUNT from MONTH_LOAN_PAYMENT"
    rs=sql_handle.execute(sql_string)

    for row in rs:
        loan_id_supposed_to_pay_list.append(int(row[0]))
        old_loan_id_to_coll_succ.update( { row[0] : row[1] })
        old_loan_id_to_coll_miss.update( { row[0] : row[2] })
        old_loan_id_to_coll_amnt.update( { row[0] : row[3] })

getTableInfo(sql_handle)

def getdefaulterList():
    global defaulter_list
    defaulter_list = list(set(loan_id_supposed_to_pay_list)-set(loan_id_paid_list))

getdefaulterList()

def updateDefaulterData(sql_handle):
    defaulter_list.sort()
    for dafaulter_loan_id in defaulter_list:
        previous_missed_count = old_loan_id_to_coll_miss[dafaulter_loan_id]
        new_missed_count = previous_missed_count + 1
        sql_string = "UPDATE MONTH_LOAN_PAYMENT SET COLLECTION_MISSED = " + str(new_missed_count) + " where LOAN_ID = " + str(dafaulter_loan_id)
        sql_handle.execute (sql_string)

updateDefaulterData(sql_handle)


def updatePayerData(sql_handle):
    loan_id_paid_list.sort()
    for payer_loan_id in loan_id_paid_list:
        previous_collection_value = old_loan_id_to_coll_amnt[payer_loan_id]
        previous_collection_count = old_loan_id_to_coll_succ[payer_loan_id]
        today_collection_value = loan_id_to_collection_dict[payer_loan_id]
        new_collection_value = previous_collection_value + today_collection_value
        new_collection_count = previous_collection_count + 1
        sql_string = "UPDATE MONTH_LOAN_PAYMENT SET COLLECTION_COUNT = " + str(new_collection_count) + ", COLLECTION_AMOUNT =" + str(new_collection_value) + " where LOAN_ID = " + str(payer_loan_id)
        sql_handle.execute( sql_string)

updatePayerData(sql_handle)


def get_collection(sql_handle):
    sql_string = "SELECT COLLECTION_AMOUNT from COLLECTIONS"
    rs=sql_handle.execute (sql_string)
    for row in rs:
        amount = row[0]
        float(amount)
        global total_collection_day
        global collection_amt
        collection_amt = total_collection_day + float(amount)

get_collection(sql_handle)

def update_total_collection(sql_handle):
    sql_string="INSERT into COLLECTIONS \
            (COLLECTION_DATE, COLLECTION_AMOUNT) values \
            ( \"" + str_day  + "\" ," + str(collection_amt) + " )"
    rs=sql_handle.execute (sql_string)
update_total_collections(sql_handle)

global collection_amt_loan 
collection_amt_loan = 0.0
def get_collection_loan(sql_handle):
    sql_string = "SELECT COLLECTION_AMOUNT from COLLECTIONS_LOAN"
    rs=sql_handle.execute (sql_string)
    for row in rs:
        amount = row[0]
        float(amount)
        global total_collection_day
        collection_amt_loan = total_collection_day + float(amount)

get_collection_loan(sql_handle)

def update_total_collections_loan(sql_handle):
    sql_string = "INSERT into COLLECTIONS_LOAN (COLLECTION_DATE, COLLECTION_AMOUNT) VALUES ( \"" + str_day + "\" ," + str(collection_amt_loan) + " )"
    print sql_string
    rs=sql_handle.execute (sql_string)

update_total_collections_loan(sql_handle)
