#!/usr/bin/python

from datetime import datetime
import sys
import sqlalchemy as db
import math
now = datetime.now()
now = now.strftime("%d %B, %Y - %H:%M:%S")
FILE_LOC = "/home/sauronil/excel_csv/rd_initiation_csv/rd_push.csv"
log_FILE_LOC = "/home/logs/PUSHER_LOGS/rd.log"

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
connection_str = "mysql+pymysql://" + db_user + ":" + db_pwd + "@" + db_host + ":" + str(db_port) + "/" + db_name
engine = db.create_engine(connection_str)
connection = engine.connect()


file_handle = open(FILE_LOC, 'r')

lines = file_handle.readlines()

count = 0

for line in lines:
    if (count > 0):

        data_list = line.split(',')

        rd_name = data_list[0].strip(' ')
        init_date = data_list[1].strip(' ')
        update_last_inter_date = data_list[1].strip(' ')
        plan_close_date = data_list[2].strip(' ')
        rate = data_list[3].strip(' ')
        annual_inter_rate = float(rate)
        quarter_inter_rate = float(annual_inter_rate)/4
        balance = data_list[4].strip(' ')
        if (str(balance) == "") :
            balance = 0.0
        dur_mnt = data_list[5].strip(' ')
        pay_freq = data_list[6].strip(' ')
        rd_stat = data_list[7].strip(' ')
        eq_daily_installment = data_list[8].strip(' ')
        remarks = data_list[9].strip(' ')
        mem_id = data_list[10].strip(' ')
        sup_id = data_list[11].strip(' ')
        agent_id = data_list[12].strip(' ').strip('\n').strip('\r')

        sql_string = "INSERT INTO RECCURING_DEPOSITS (RD_NAME, INITIATION_DATE, LAST_INTEREST_UPDATE_DATE , PLANNED_CLOSING_DATE, ANNUAL_INTEREST_RATE, QUARTER_INTEREST_RATE, BALANCE, DURATION_MONTHS, PAYMENT_FREQUENCY, RD_STATUS, EQUAL_DAILY_INSTALLMENT, REMARKS, MEMBER_ID, SUPERVISOR_ID, AGENT_ID ) " 

        values = "VALUES (\"" + rd_name + "\", \"" + init_date + "\", \"" + update_last_inter_date + "\",  \"" + plan_close_date +  "\"" + ", "  + str(annual_inter_rate) + "," + str(quarter_inter_rate) + "," + str(balance) + ", \"" + dur_mnt +  "\"" + ", \""  + pay_freq  + "\", \""  +  rd_stat  + "\", " + str(eq_daily_installment) + ", \"" + remarks + "\", "  +  str(mem_id)   + "," + str(sup_id)  + ", " +  str(agent_id)  +     ") "

        sql_string = sql_string + values
        sys.stdout=open(log_FILE_LOC, 'a')
        print now, sql_string
        sys.stdout.close()
        rs=connection.execute (sql_string)
    
    count+=1
