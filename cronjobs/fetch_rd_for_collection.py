#!/usr/bin/python
import calendar
import datetime
import sqlalchemy as db

file_loc= "/home/BALAJI/input/rd/PCTX.TXT"
d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")
config = {
         'host': '192.168.122.111',
         'port': 3306,
         'user': 'xaraticli',
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

rds = []

def get_active_rd(sql_handle):
    sql_string = "SELECT RD_ID from RECCURING_DEPOSITS where RD_STATUS=\'Active\'"
    rs=sql_handle.execute (sql_string)
    for row in rs:
        rds.append(row[0])
get_active_rd(sql_handle)

rd_id_to_member = {}
rd_id_to_balance = {}
rd_id_to_name = {}
rd_id_to_initiation_date = {}
rd_id_to_agent_id = {}


def fetch_device_feed_rd_info(sql_handle):
    for rd in rds:
        sql_string = "SELECT RD_ID, BALANCE, INITIATION_DATE, MEMBER_ID from RECCURING_DEPOSITS where RD_ID = " + str(rd)
        rs = sql_handle.execute (sql_string)
        for row in rs:
            this_rd = row[0]
            rd_id_to_balance.update({row[0]: row[1]})
            rd_id_to_initiation_date.update({row[0]: row[2]})
            rd_id_to_member.update({row[0]: row[3]})
        for rd_id in rd_id_to_member:
            this_member_id = rd_id_to_member[rd_id]
            sql_string = "SELECT AGENT_ID, FIRST_NAME from MEMBERS where MEMBER_ID =" + str(this_member_id)

            rs=sql_handle.execute (sql_string)
            for row in rs:
                rd_id_to_name.update( { rd_id : row[1]})
                rd_id_to_agent_id.update({rd_id : row[0]})


fetch_device_feed_rd_info(sql_handle)

def agent():

    holiday=str("12341234")
    agent_acc_no="101"
    ten_blank_spaces=" " * 10
    agent_code_bank_code="110110"
    agent_str=str(agent_acc_no).zfill(6) +","+"000000,000000" +str(ten_blank_spaces)+","+agent_code_bank_code+","+str(d.strftime('%d.%m.%y')) + "," + str(holiday)+ str("\n")
    return agent_str

    
def client():

    fp=open(file_loc, 'w')
    fp.write(agent())
    rds.sort()
    for rd in rds:
        account_no=rd_id_to_member[rd]
        id_print = str(account_no).zfill(6)
        collection="000000"
        customer_name=rd_id_to_name[rd]
        blank_space_len=16-len(customer_name)
        blank_space_to_print=" " * blank_space_len
        balance = int(rd_id_to_balance[rd])
        bal=str(balance).zfill(6)
        initiation_date=str(rd_id_to_initiation_date[rd].strftime('%d.%m.%y'))
        collection_amount="000000"
        fp.write(str(id_print) + "," + str(collection) \
            + "," + str(customer_name)+ str(blank_space_to_print) \
            + "," + str(bal) + "," + str(initiation_date) \
            + "," + str(collection_amount) + str("  \n"))
    fp.write(b'\x04')

client()
