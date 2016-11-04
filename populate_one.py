import mysql.connector
from CapstoneProject.settings import DATABASES
import os


def populate_initial_data(stock_file, ticker):
    conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
    cursor = conn.cursor()
    f2 = open(stock_file,'r')
    records = f2.read().split("\n")
    for i in xrange(len(records)-2,0,-1):
        ohlc = records[i].split(",")
        cursor.execute("INSERT INTO OHLC (`sec_id`,`date`,`open`,`high`,`low`,`close`) VALUES"\
                    + "((select id from security where yahoo_ticker='"+ticker+"'),'"+ohlc[0]+"',"+ohlc[1]+","+ohlc[2]+","+ohlc[3]+","+ohlc[4]+")")
    f2.close()
    conn.commit()
    conn.close()


populate_initial_data("stock_data/FTSE100/IHG.csv", "IHG")
