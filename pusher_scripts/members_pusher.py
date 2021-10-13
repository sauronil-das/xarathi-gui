#!/usr/bin/python
from datetime import datetime
import sys
import sqlalchemy as db
import math

now = datetime.now()
now = now.strftime("%d %B, %Y - %H:%M:%S")

FILE_LOC = "/home/sauronil/excel_csv/member_data_exel_csv/member_push.csv"
log_FILE_LOC = "/home/logs/PUSHER_LOGS/member.log"
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

        fname =           data_list[0].strip(' ')
        lname =           data_list[1].strip(' ')
        b_day =           data_list[2].strip(' ')
        mem_date =        data_list[3].strip(' ')
        per_addr =        data_list[4].strip(' ')
        curr_addr =       data_list[5].strip(' ')
        stock_no =        data_list[6].strip(' ')
        per_stock_value = data_list[7].strip(' ')
        agent_id =        data_list[8].strip(' ').strip('\n').strip('\r')

        sql_string = "INSERT INTO MEMBERS \
                ( FIRST_NAME, LAST_NAME, BIRTH_DATE, MEMBERSHIP_DATE, PERMANENT_ADDRESS, CURRENT_ADDRESS, STOCK_NUM, PER_STOCK_VALUE, AGENT_ID) VALUES \
                ( \"" +  fname + "\", \"" + lname + "\", \"" + b_day + "\", \"" + mem_date + "\", \"" + per_addr + "\", \"" + curr_addr + "\", " + stock_no + ", " + per_stock_value + ", " + agent_id + " )"
        sys.stdout=open(log_FILE_LOC, 'a')
        print now, sql_string
        sys.stdout.close()

        rs=connection.execute(sql_string)

    count+=1


