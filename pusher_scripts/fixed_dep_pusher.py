#!/usr/bin/python
from datetime import datetime
import sys
import sqlalchemy as db
import math

now = datetime.now()
now = now.strftime("%d %B, %Y - %H:%M:%S")

FILE_LOC = "/home/sauronil/excel_csv/fixed_deposit_pusher/fixed_dep_pusher.csv"
log_FILE_LOC = "/home/logs/PUSHER_LOGS/fixed_deposit.log"

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


file_handle = open (FILE_LOC, 'r')

lines=file_handle.readlines()

count = 0

for line in lines:
    if(count>0) :

        data_list = line.split(',')

        fd_name = data_list[0].strip(' ')
        join_date = data_list[1]
        last_inter_update_date = data_list[1]
        planned_close_date = data_list[2]
        ann_inter_rate = data_list[3].strip(' ')
        balance = data_list[4].strip(' ')
        fd_stat = data_list[5].strip(' ')
        remarks = data_list[6].strip(' ')
        mem_id = data_list[7].strip(' ')
        sup_id = data_list[8].strip(' ')
        agent_id = data_list[9].strip(' ').strip('\n').strip('\r')

        sql_string = "INSERT INTO FIXED_DEPOSIT (FD_NAME, INITIATION_DATE, LAST_INTEREST_UPDATE_DATE, PLANNED_CLOSING_DATE, ANNUAL_INTEREST_RATE, BALANCE, FD_STATUS, REMARKS, MEMBER_ID, SUPERVISOR_ID, AGENT_ID ) VALUES ( \"" + fd_name+ "\", \"" +  join_date  + "\", \"" + last_inter_update_date + "\", \"" + planned_close_date   + "\", " + ann_inter_rate + "," + balance  + ", \"" + fd_stat  + "\", \"" + remarks + "\", " + mem_id  + ", " + sup_id + ", " + agent_id + ")"
        sys.stdout=open(log_FILE_LOC, 'a')
        print now, sql_string
        sys.stdout.close()
        rs=connection.execute (sql_string)

    count+=1





