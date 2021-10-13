#!/usr/bin/python
from datetime import datetime
import sys
import sqlalchemy as db
import math

now = datetime.now()
now = now.strftime("%d %B, %Y - %H:%M:%S")

FILE_LOC = "/home/sauronil/excel_csv/loan_initiation_csv/loan_push.csv"
log_FILE_LOC = "/home/logs/PUSHER_LOGS/loan.log"

config = {
        'host': '192.168.122.111',
        'port': 3306,
        'user': 'xaraticli',
        'password': 'SmellyCatSmellyCat',
        'database': 'NIDHI_BANK'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

def current_month_interest(principal, annual_interest_rate):
     monthly_interest = annual_interest_rate / 12
     interest = (monthly_interest/100) * principal
     return interest

def equal_monthly_installment(principal, annual_interest_rate, duration_month):
     monthly_interest = annual_interest_rate / 12
     R = monthly_interest / 100
     one_plus_r_pow_n = pow(1+R , duration_month)
     one_plus_r_pow_n_minus_one = one_plus_r_pow_n - 1
     emi = (principal * R * one_plus_r_pow_n) / one_plus_r_pow_n_minus_one
     return emi


connect_str= "mysql+pymysql://" + db_user + ":" + db_pwd + "@" + db_host + ":" + str(db_port) + "/" + db_name
engine = db.create_engine(connect_str)

connection = engine.connect()

file_handle = open(FILE_LOC, 'r')

lines = file_handle.readlines()

count=0

#stripping new lines

for line in lines:
    if(count>0):

        data_list = line.split(',')

        loan_name =          data_list[0].strip(' ')
        member_id =          data_list[1].strip(' ')
        annual_inter_rate =  data_list[2].strip(' ')
        principal_amt =      data_list[3].strip(' ')
        process_fee =        data_list[4].strip(' ')
        initial_date =       data_list[5].strip(' ')
        mnt_dur =            data_list[6].strip(' ')
        pay_freq =           data_list[7].strip(' ')
        loan_stat =          data_list[8].strip(' ')
        remarks =            data_list[9].strip(' ')
        sup_id =             data_list[10].strip(' ')
        agent_id =           data_list[11].strip(' ').strip('\n').strip('\r')
        
        my_mnt_dur = float(mnt_dur)

        my_emi          = equal_monthly_installment(float(principal_amt), float(annual_inter_rate), float(my_mnt_dur))
        int_curr_mnt    = current_month_interest(float(principal_amt), float(annual_inter_rate))
        pri_ded_cur_mnt = my_emi - int_curr_mnt

        sql_string= "INSERT INTO LOANS \
                ( LOAN_NAME, MEMBER_ID, ANNUAL_INTEREST_RATE, PRINCIPAL, PRINCIPAL_BALANCE, EQUAL_MONTHLY_INSTALLMENT, INTEREST_CURRENT_MONTH, PRINCIPAL_DEDUCTION_CURRENT_MONTH, PROCESSING_FEE, INITIATION_DATE, DURATION_MONTH, PAYMENT_FREQUENCY, LOAN_STATUS, REMARKS, SUPERVISOR_ID, AGENT_ID) VALUES \
                ( \"" + loan_name + "\", " + member_id + ", " + annual_inter_rate + ", " + principal_amt + ", " + principal_amt + ", " +  str(my_emi) + ", " + str(int_curr_mnt) + ", " + str(pri_ded_cur_mnt) + ", " + process_fee + ", \"" + initial_date + "\", " + mnt_dur + ", \"" + pay_freq + "\", \"" + loan_stat + "\", \"" + remarks + "\", " + sup_id + ", " + agent_id + " )"
        sys.stdout=open(log_FILE_LOC, 'a')
        print now, sql_string
        sys.stdout.close()
        rs=connection.execute(sql_string)

    count+=1
