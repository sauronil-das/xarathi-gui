#!/usr/bin/python
import calendar
from datetime import date, timedelta
import sys
import datetime
import sqlalchemy as db

d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")


log_FILE_LOC = "/home/logs/RECONCILE_LOGS/fixed_deposit.log"
# specify database configurations
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
    
sql_handle = connect()


fixed_deposit = []

fd_id_to_balance = {}
fd_id_to_total_amount = {}
fd_id_to_interest_rate = {}
fd_id_to_last_inter_update_date = {}

def addYears(d, years):

    try: 
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def get_fd(sql_handle):

    sql_string = "SELECT FD_ID, ANNUAL_INTEREST_RATE, TOTAL_INTEREST, BALANCE, LAST_INTEREST_UPDATE_DATE from FIXED_DEPOSIT"
    rs=sql_handle.execute (sql_string)
    for row in rs:
        fixed_deposit.append(row[0])
        fd_id_to_interest_rate.update({row[0]: row[1]})
        fd_id_to_total_amount.update({row[0]: row[2]})
        fd_id_to_balance.update({ row[0] : row[3]})
        fd_id_to_last_inter_update_date.update({row[0]: row[4]})
        date = fd_id_to_last_inter_update_date[row[0]]
        str_date = str(date)
        values = str_date.split('-')
        year =  values[0]
        month = values[1]
        day = values[2]
        update_date = addYears(datetime.date(int(year), int(month), int(day)), 1)
        
        fd_id_to_last_inter_update_date.update({row[0]: str(update_date)})
        print fd_id_to_last_inter_update_date[row[0]] 

    return fixed_deposit

get_fd(sql_handle)


new_fd_balance = {}
new_fd_total_amount = {}



def update_fd(sql_handle):
    fixed_deposit.sort()
    for deposit in fixed_deposit:
        date_time = now.strftime("%Y-%m-%d")
        if (date_time == fd_id_to_last_inter_update_date[deposit]):
            update_date = fd_id_to_last_inter_update_date[deposit]
            inter_amt = fd_id_to_total_amount[deposit]
            balance = fd_id_to_balance[deposit]
            rate = fd_id_to_interest_rate[deposit]
            inter_amt = float(balance) * (float(rate)/100) * 1
            balance = balance + inter_amt
            new_fd_balance.update({deposit: balance })
            new_fd_total_amount.update({deposit : inter_amt})
            sql_string = "UPDATE FIXED_DEPOSIT SET BALANCE = " + str(new_fd_balance[deposit]) + ", TOTAL_INTEREST = " + str(new_fd_total_amount[deposit]) + ", LAST_INTEREST_UPDATE_DATE = " +  str(update_date) + " WHERE FD_ID = " + str(deposit) 
            sys.stdout = open(log_FILE_LOC, 'a')
            print now, sql_string
            sys.stdout.close()
        sql_handle.execute (sql_string)
update_fd(sql_handle)


