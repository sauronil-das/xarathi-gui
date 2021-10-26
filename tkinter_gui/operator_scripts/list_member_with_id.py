#!/usr/bin/python
from prettytable import PrettyTable
import sqlalchemy as db
import sys

mem_id=sys.argv[1]

print mem_id

config = {
     'host' : '192.168.122.111',
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
sql_handle=connect()


def list_member(sql_handle):
	sql_string = "select * from MEMBERS where MEMBER_ID=" + str(mem_id)
	rs=sql_handle.execute(sql_string)
	x=PrettyTable()
	x.field_names = ["MEMBER_ID", "AGENT_ID", "FIRST_NAME", "LAST_NAME", "BIRTH_DATE", "MEMBERSHIP_DATE", "TERMINATION_DATE",
			 "STOCK_NUM", "PER_STOCK_VALUE", "PERMANENT_ADDRESS", "CURRENT_ADDRESS"]
	for row in rs:
		x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
	
	print (x)


list_member(sql_handle)
