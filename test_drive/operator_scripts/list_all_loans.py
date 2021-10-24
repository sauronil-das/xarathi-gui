#!/usr/bin/python
from prettytable import PrettyTable
import sqlalchemy as db


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


def list_all_loan(sql_handle):
	sql_string = "select LOANS.MEMBER_ID, FIRST_NAME, LAST_NAME, LOAN_ID, INITIATION_DATE, PRINCIPAL, PROCESSING_FEE, INTEREST_CURRENT_MONTH, TOTAL_COLLECTION, PENALTY FROM LOANS LEFT JOIN MEMBERS ON LOANS.MEMBER_ID = MEMBERS.MEMBER_ID ORDER BY LOANS.MEMBER_ID ASC"
	rs=sql_handle.execute(sql_string)
	x=PrettyTable()
	x.field_names = ["MEMBER_ID", "FIRST_NAME", "LAST_NAME", "LOAN_ID", "INITIATION_DATE", "PRINCIPAL", "PROCESSING_FEE", "INTEREST_CURRENT_MONTH", "TOTAL_COLLECTION", "PENALTY"]
	for row in rs:
		x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
	
	print (x)


list_all_loan(sql_handle)
