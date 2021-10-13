#!/usr/bin/python
import calendar
import sys
import datetime
import sqlalchemy as db

d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")


log_FILE_LOC = "/home/logs/RECONCILE_LOGS/loans.log"
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
    print connection_str
    engine = db.create_engine(connection_str)
    connection = engine.connect()
    return connection

sql_handle = connect()

loans = []
loan_id_to_collection_made = {}
loan_id_to_collection_missed = {}
loan_id_to_collection_amount = {}

def get_active_loan_collection(sql_handle):
    sql_string = "SELECT LOAN_ID, COLLECTION_COUNT, COLLECTION_MISSED, COLLECTION_AMOUNT from MONTH_LOAN_PAYMENT"
    rs = sql_handle.execute (sql_string)
    for row in rs:
        loans.append(row[0])
        loan_id_to_collection_made.update( {row[0] : row[1]} )
        loan_id_to_collection_missed.update( {row[0] : row[2]} )
        loan_id_to_collection_amount.update( {row[0] : row[3]} )
    return loans

get_active_loan_collection(sql_handle)

#print "loan_id_to_collection_amount: " + str(loan_id_to_collection_amount)

loan_id_to_principal_balance = {}
loan_id_to_int_curr_month = {}
loan_id_to_principal_ded_curr_month = {}
loan_id_to_num_payments_made = {}
loan_id_to_num_paymens_missed = {}
loan_id_to_emi = {}

def get_loan_data(sql_handle):
    for loan in loans:
        sql_string = "SELECT LOAN_ID, PRINCIPAL_BALANCE, INTEREST_CURRENT_MONTH, PRINCIPAL_DEDUCTION_CURRENT_MONTH, PAYMENTS_MADE, PAYMENTS_MISSED, EQUAL_MONTHLY_INSTALLMENT from LOANS where LOAN_ID = " + str(loan)
        rs = sql_handle.execute (sql_string)
        for row in rs:
            loan_id_to_principal_balance.update( {row[0] : row[1]} )
            loan_id_to_int_curr_month.update( {row[0] : row[2]} )
            loan_id_to_principal_ded_curr_month.update( {row[0] : row[2]} )
            loan_id_to_num_payments_made.update( {row[0] : row[4]} )
            loan_id_to_num_paymens_missed.update( {row[0] : row[5]} )
            loan_id_to_emi.update( {row[0] : row[5]})

get_loan_data(sql_handle)

fresh_num_payments = {}
fresh_num_missed_payments = {}
fresh_principal = {}
def update_loan_values(sql_handle):
    loans.sort()
    for loan in loans:
        fresh_num_payments.update( { loan : (int(loan_id_to_num_payments_made[loan]) + int(loan_id_to_collection_made[loan])) } )
        fresh_num_missed_payments.update( { loan : (int(loan_id_to_num_paymens_missed[loan]) + int(loan_id_to_collection_missed[loan])) } )
        collection_minus_interest = loan_id_to_collection_amount[loan] - loan_id_to_int_curr_month[loan]
        #print "collection_minus_interest: " + str(collection_minus_interest)
        new_principal = loan_id_to_principal_balance[loan] - collection_minus_interest
        #print "new_principal: " + str(new_principal)
        fresh_principal.update( { loan : new_principal } )

update_loan_values(sql_handle)

def update_loan_table(sql_handle):
    loans.sort()
    for loan in loans:
        sql_string = "UPDATE LOANS SET PRINCIPAL_BALANCE = " + str(fresh_principal[loan]) + ", PAYMENTS_MADE = " + str(fresh_num_payments[loan]) + ", PAYMENTS_MISSED = " + str(fresh_num_missed_payments[loan]) + " where LOAN_ID = " + str(loan)
        #print sql_string
        sql_handle.execute (sql_string)
        
update_loan_table(sql_handle)

#def delete_loan_collection(sql_handle, loans):
#    loans.sort()
#    for loan_id in loans:
#        sql_string = "DELETE from MONTH_LOAN_PAYMENT where LOAN_ID = " + str(loan_id)
#        sql_handle.execute (sql_string)

#delete_loan_collection(sql_handle, loans)

def current_month_interest(principal, annual_interest_rate):
    monthly_interest = annual_interest_rate / 12
    interest = (monthly_interest/100) * principal
    return interest

loan_to_int_this_month = {}
loan_to_pri_ded_this_month = {}
def get_new_interst_and_pri_ded(sql_handle, loans):
    loans.sort()
    for loan in loans:
        sql_string = "SELECT ANNUAL_INTEREST_RATE, PRINCIPAL_BALANCE, EQUAL_MONTHLY_INSTALLMENT from LOANS where LOAN_ID = " + str(loan)
        #print sql_string
        rs = sql_handle.execute (sql_string)
        for row in rs:
            #print current_month_interest(row[1], row[0])
            loan_to_int_this_month.update( { loan : current_month_interest(row[1], row[0]) } )
            loan_to_pri_ded_this_month.update ( { loan : (row[2] - current_month_interest(row[1], row[0]) )} )

get_new_interst_and_pri_ded(sql_handle, loans)
    
#print "loan_to_int_this_month: " + str(loan_to_int_this_month)
#print "loan_to_pri_ded_this_month: " + str(loan_to_pri_ded_this_month)

def update_loan_with_new_interest(sql_handle, loans):
    loans.sort()
    for loan in loans:
        sql_string = "UPDATE LOANS SET INTEREST_CURRENT_MONTH = " + str(loan_to_int_this_month[loan]) + " , PRINCIPAL_DEDUCTION_CURRENT_MONTH = " + str(loan_to_pri_ded_this_month[loan]) + " where LOAN_ID = " + str(loan)
        #print sql_string
        sql_handle.execute (sql_string)

update_loan_with_new_interest(sql_handle, loans)

sys.stdout=open(log_FILE_LOC, 'a')
log_string = "This reconcile was initiated by $USER on - "
print log_string, now
sys.stdout.close()
