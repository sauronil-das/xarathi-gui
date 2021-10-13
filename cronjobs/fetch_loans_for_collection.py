#!/usr/bin/python
import calendar
import datetime
import sqlalchemy as db


file_loc='/home/BALAJI/input/loans/PCTX.TXT'

d= datetime.datetime.now()
now = d.strftime("%d %B, %Y")

# specify database configurations
config = {
    'host':'192.168.122.111',
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

sql_handle = connect()

loans = []

def get_active_loan_collection(sql_handle):
    sql_string = "SELECT LOAN_ID from MONTH_LOAN_PAYMENT"
    rs = sql_handle.execute (sql_string)
    for row in rs:
        loans.append(row[0])

get_active_loan_collection(sql_handle)
#print "loans: " + str(loans)

loan_id_to_member = {}
loan_id_to_balance = {}
loan_id_to_name = {}
loan_id_to_agent_id = {}
loan_id_to_initiation_date = {}

def fetch_device_feed_loan_info(sql_handle):
    for loan in loans:
        sql_string = "SELECT LOAN_ID, PRINCIPAL_BALANCE, INTEREST_CURRENT_MONTH, MEMBER_ID, INITIATION_DATE from LOANS where LOAN_ID = " + str(loan)
        rs = sql_handle.execute (sql_string)
        for row in rs:
            this_loan = row[0]
            loan_id_to_balance.update( { row[0] : row[1] + row[2] } )
            loan_id_to_member.update( {row[0] : row[3] })
            loan_id_to_initiation_date.update( {row[0] : row[4] } )
        for loan_id in loan_id_to_member:
            this_member_id = loan_id_to_member[loan_id]
            sql_string = "SELECT AGENT_ID, FIRST_NAME, LAST_NAME from MEMBERS where MEMBER_ID = " + str(this_member_id)
            rs = sql_handle.execute (sql_string)
            for row in rs:
                loan_id_to_name.update( { loan_id : row[1]})
                loan_id_to_agent_id.update( { loan_id : row[0]} )

fetch_device_feed_loan_info(sql_handle)

#print "loan_id_to_member: " +  str(loan_id_to_member)
#print "loan_id_to_balance: " + str(loan_id_to_balance)
#print "loan_id_to_name: " + str(loan_id_to_name)
#print "loan_id_to_agent_id: " + str(loan_id_to_agent_id)
#print "loan_id_to_initiation_date: " + str(loan_id_to_initiation_date)

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
    loans.sort()
    for loan in loans:
        account_no=loan
        id_print = str(account_no).zfill(6)
        collection="000000"
        customer_name=loan_id_to_name[loan]
        blank_space_len=16-len(customer_name)
        blank_space_to_print=" " * blank_space_len
        int_balance=int(loan_id_to_balance[loan])
        balance=str(int_balance).zfill(6)
        initiation_date=str(loan_id_to_initiation_date[loan].strftime
                ('%d.%m.%y'))
        collection_amount="000000"

        fp.write(str(id_print) + "," + str(collection) \
                + "," + str(customer_name)+ str(blank_space_to_print) \
                + "," + str(balance) + "," + str(initiation_date) \
                + "," + str(collection_amount) + str(" ") + str("  \n"))
    fp.write(b'\x04')
   

client()
