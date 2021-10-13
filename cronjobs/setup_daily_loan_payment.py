#!/usr/bin/python
import calendar
import datetime
import sqlalchemy as db
import sys
now = datetime.datetime.now()
day_num_in_month =  calendar.monthrange(now.year, now.month)[1]
log_FILE_LOC = "/home/logs/RECONCILE_LOGS/setup_daily_loans.log"
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

loan_id_to_emi_dict = {}
def get_active_loans(sql_handle):
    sql_string = "SELECT LOAN_ID from LOANS where LOAN_STATUS=\'Active\' AND PRINCIPAL_BALANCE > 0"
    rs = sql_handle.execute (sql_string)
    loans = []
    for row in rs:
        loans.append(row[0])
    return loans

def get_npa_loans(sql_handle):
    sql_string = "SELECT LOAN_ID from LOANS where LOAN_STATUS=\'NPA\' AND PRINCIPAL_BALANCE > 0"
    rs = sql_handle.execute (sql_string)
    loans = []
    for row in rs:
        loans.append(row[0])
    return loans

def get_stressed_loans(sql_handle):
    sql_string = "SELECT LOAN_ID from LOANS where LOAN_STATUS=\'Stressed\' AND PRINCIPAL_BALANCE > 0"
    rs = sql_handle.execute (sql_string)
    loans = []
    for row in rs:
        loans.append(row[0])
    return loans

def delete_loan_collection(sql_handle, loans):
    for loan_id in loans:
        sql_string = "DELETE from MONTH_LOAN_PAYMENT where LOAN_ID = " + str(loan_id)
        sql_handle.execute (sql_string)

def load_emi_payment(sql_handle, loans): 
    for loan_id in loans:
        sql_string = "SELECT EQUAL_MONTHLY_INSTALLMENT from LOANS where LOAN_ID = " + str(loan_id)
        rs = sql_handle.execute (sql_string)
        for row in rs:
            loan_id_to_emi_dict.update( {loan_id : row[0]} )

def load_daily_payment(sql_handle, loan_id_to_emi_dict):
    loan_id_to_emi_dict
    for loan_id in loan_id_to_emi_dict:
        per_day_collection = loan_id_to_emi_dict[loan_id] / day_num_in_month
        sql_string = "INSERT into MONTH_LOAN_PAYMENT (LOAN_ID , COLLECTION_MONTH_YEAR, COLLECTION_PER_DAY, DAYS) VALUES (" + str(loan_id) + " , now(), " + str(per_day_collection) + ", " + str(day_num_in_month) + ")"
        sql_handle.execute (sql_string)


active_loans =  get_active_loans(sql_handle)
npa_loans = get_npa_loans(sql_handle)
stressed_loans = get_stressed_loans(sql_handle)

all_loans = []

all_loans.extend(active_loans) 
all_loans.extend(npa_loans) 
all_loans.extend(stressed_loans)

delete_loan_collection(sql_handle, active_loans)
delete_loan_collection(sql_handle, npa_loans)
delete_loan_collection(sql_handle, stressed_loans)


load_emi_payment(sql_handle, active_loans)
load_emi_payment(sql_handle, npa_loans)
load_emi_payment(sql_handle, stressed_loans)

load_daily_payment(sql_handle,loan_id_to_emi_dict)

d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")

log_string = "Setup Loan Payment was initiated by $USER on - "
sys.stdout=open(log_FILE_LOC, 'a')
print log_string, now
sys.stdout.close()
