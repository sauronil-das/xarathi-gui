#!/usr/bin/python
from datetime import datetime
import sys
import sqlalchemy as db
import math

now = datetime.now()
now = now.strftime("%d %B, %Y - %H:%M:%S")
FILE_LOC = "/home/sauronil/excel_csv/supervisor_data_exel_csv/supers_push.csv"
log_FILE_LOC = "/home/logs/PUSHER_LOGS/supervisor.log"
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
# Strips the newline character
for line in lines:
    if (count > 0) :
        data_list = line.split(',')
        fname = data_list[0].strip(' ')
        lname = data_list[1].strip(' ')
        bdate = data_list[2]
        jdate = data_list[3]
        paddr = data_list[4].strip(' ')
        caddr = data_list[5].strip(' ').strip('\n').strip('\r')
        sql_string = "INSERT INTO SUPERVISORS \
                      ( FIRST_NAME, LAST_NAME, BIRTH_DATE, JOINING_DATE, PERMANENT_ADDRESS, CURRENT_ADDRESS) VALUES \
                      ( \"" + fname + "\" , \"" + lname + "\", \"" + bdate + "\" , \"" + jdate + "\", \"" + paddr + "\" , \"" + caddr + "\" )"
        sys.stdout=open(log_FILE_LOC, 'a')
        print now, sql_string
        sys.stdout.close()
        rs = connection.execute (sql_string)
    count += 1
