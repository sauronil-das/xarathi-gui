#!/usr/bin/python

import sqlalchemy as db
import sys

amount=sys.argv[1]
rd_id=sys.argv[2]

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


def update_rd(sql_handle):
	sql_string="update RECCURING_DEPOSITS set BALANCE =" + str(amount) + " where RD_ID= " + str(rd_id)
	rs=sql_handle.execute(sql_string)


update_rd(sql_handle)
