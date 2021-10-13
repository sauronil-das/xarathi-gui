#!/usr/bin/python
import calendar
from datetime import date, timedelta
import sys
import datetime
from dateutil.relativedelta import relativedelta
import sqlalchemy as db
d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")

log_FILE_LOC = "/home/logs/RECONCILE_LOGS/rd.log"
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

rds = []

rd_id_to_balance = {}
rd_id_to_quarter_interest_rate = {}
rd_id_to_last_inter_update_date = {}

def add_three_months(date):
    str_date = str(date)
    values = str_date.split('-')
    year = values[0]
    month = values[1]
    day = values[2]
    d=datetime.datetime(int(year), int(month), int(day))
    newday = d.day
    newmonth = (((d.month - 1) + 3 ) % 12) + 1
    newyear = d.year + (((d.month - 1) + 3) // 12)
    if(newday > calendar.mdays[newmonth]):
        newday = calendar.mdays[newmonth]
        if (newyear % 4 == 0 and newmonth == 2):
            newday+=1
    val = datetime.date(newyear, newmonth, newday)
    return str(val)
def get_rd(sql_handle):
    sql_string = "SELECT RD_ID, BALANCE, QUARTER_INTEREST_RATE, LAST_INTEREST_UPDATE_DATE from RECCURING_DEPOSITS"
    rs=sql_handle.execute (sql_string)
    for row in rs:
        rds.append(row[0])
        rd_id_to_balance.update({row[0]: row[1]})
        rd_id_to_quarter_interest_rate.update({row[0]: row[2]})
        rd_id_to_last_inter_update_date.update({row[0]: str(row[3])})
        three_months =add_three_months(rd_id_to_last_inter_update_date[row[0]])
        rd_id_to_last_inter_update_date.update({row[0]: three_months})
    return rds

get_rd(sql_handle)

new_rd_balance = {}

def update_rd(sql_handle):
    rds.sort()
    for rd in rds:
        date_time=now.strftime("%Y-%m-%d")
        if(date_time == rd_id_to_last_inter_update_date[rd]):
            last_inter_update_date = rd_id_to_last_inter_update_date[rd]
            balance = rd_id_to_balance[rd]
            rate = rd_id_to_quarter_interest_rate[rd]
            inter_amt = float(balance) * (float(rate)/100) * 1
            balance = balance + inter_amt
            rd_id_to_balance.update({rd: balance})
            sql_string =  "UPDATE RECCURING_DEPOSITS SET BALANCE = " + str(rd_id_to_balance[rd]) + ", LAST_INTEREST_UPDATE_DATE = " + str(rd_id_to_last_inter_update_date[rd]) 
        sql_handle.execute (sql_handle)

update_rd(sql_handle)

sys.stdout=open(log_FILE_LOC, 'a')
log_string = "Recurring Deposit was initiated by $USER on - "
print log_string, now
sys.stdout.close()
