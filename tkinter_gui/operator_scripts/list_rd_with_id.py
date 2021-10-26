#!/usr/bin/python
from prettytable import PrettyTable
import sqlalchemy as db
import sys

mem_id=sys.argv[1]

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


def list_rd_id(sql_handle):
	sql_string = "select * from RECCURING_DEPOSITS where MEMBER_ID=" + str(mem_id)
	rs=sql_handle.execute(sql_string)
	x=PrettyTable()
	x.field_names = ["RD_ID", "RD_NAME", "INITIATION_DATE", "LAST_INTEREST_UPDATE_DATE", "PLANNED_CLOSING_DATE", "ANNUAL_INTEREST_RATE",
			 "QUARTER_INTEREST_RATE", "BALANCE", "DURATION_MONTHS", "PAYMENT_FREQUENCY", "PAYMENTS_MADE", "PAYMENTS_MISSED", 
			 "RD_STATUS", "EQUAL_DAILY_INSTALLMENT", "PENALTY", "REMARKS", "MEMBER_ID", "SUPERVISOR_ID", "AGENT_ID"]
	for row in rs:
		x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
			  row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]])
	
	print (x)


list_rd_id(sql_handle)
