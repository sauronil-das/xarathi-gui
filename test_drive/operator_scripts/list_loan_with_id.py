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


def list_loan_id(sql_handle):
	sql_string = "select * from LOANS where MEMBER_ID=" + str(mem_id)
	rs=sql_handle.execute(sql_string)
	x=PrettyTable()
	x.field_names = ["LOAN_ID", "LOAN_NAME", "INITIATION_DATE", "ANNUAL_INTEREST_RATE", "PRINCIPAL", "DURATION_MONTH",
			 "PRINCIPAL_BALANCE", "PROCESSING_FEE", "INTEREST_CURRENT_MONTH", "PRINCIPAL_DEDUCTION_CURRENT_MONTH",
			 "PAYMENT_FREQUENCY", "PAYMENTS_MADE", "PAYMENTS_MISSED" "LOAN_STATUS", "EQUAL_MONTHLY_INSTALLMENT", 
			 "TOTAL_COLLECTION", "PENALTY", "REMARKS", "MEMBER_ID", "SUPERVISOR_ID", "AGENT_ID"]
	for row in rs:
		x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
			  row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]])
	
	print (x)


list_loan_id(sql_handle)
