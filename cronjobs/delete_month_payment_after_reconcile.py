#!/usr/bin/python
import calendar
import sys
import datetime
import sqlalchemy as db

d = datetime.datetime.now()
now = d.strftime("%d %B, %Y")
day_num_in_month =  calendar.monthrange(now.year, now.month)[1]
log_FILE_LOC = ""
class MariaConnector:
    def __init__(self):
        self.config = {
            'host': '192.168.122.111',
            'port': 3306,
            'user': 'xaraticli',
            'password': 'SmellyCatSmellyCat',
            'database': 'NIDHI_BANK'
             }
        self.connection = ""
        self.connect()

    def connect(self):
        db_user = self.config.get('user')
        db_pwd  = self.config.get('password')
        db_host = self.config.get('host')
        db_port = self.config.get('port')
        db_name = self.config.get('database')
        connection_str = "mysql+pymysql://" + db_user + ":" + db_pwd + "@" + db_host + ":" + str(db_port) + "/" + db_name
        print connection_str
        engine = db.create_engine(connection_str)
        self.connection = engine.connect()

class LoanHandler(MariaConnector):
    def __init__(self):
        MariaConnector.__init__(self)
        self.loans = []
        self.get_active_loan_collection()

    def get_active_loan_collection(self):
        sql_string = "SELECT LOAN_ID, COLLECTION_COUNT, COLLECTION_MISSED, COLLECTION_AMOUNT from MONTH_LOAN_PAYMENT"
        rs = self.connection.execute (sql_string)
        for row in rs:
            self.loans.append(row[0])
        self.loans.sort()

    def delete_loan_collection(self):
        for loan_id in self.loans:
            sql_string = "DELETE from MONTH_LOAN_PAYMENT where LOAN_ID = " + str(loan_id)
            username = "by $USER"
            sys.stdout = open(log_FILE_LOC, 'a')
            print now, sql_string, username
            sys.stdout.close()
            self.connection.execute(sql_string)

    def print_loans(self):
        print self.loans

myLoanHandler = LoanHandler()
myLoanHandler.print_loans()
myLoanHandler.delete_loan_collection()

