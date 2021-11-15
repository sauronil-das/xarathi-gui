#!/usr/bin/python

import sqlalchemy as db
import sys

loan_id=sys.argv[1]

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


def delete_loan(sql_handle):
	sql_string="update LOANS set LOAN_STATUS = \"Closed\" where LOAN_ID = " + str(loan_id)
	rs=sql_handle.execute(sql_string)


delete_loan(sql_handle)
