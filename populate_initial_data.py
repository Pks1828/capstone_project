import mysql.connector
from CapstoneProject.settings import DATABASES
import os


def populate_initial_data(index_name, index_file):
    conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
    cursor = conn.cursor()
    path = "stock_data/"+index_name.replace("&","N")+"/"
    files = os.listdir(path)
    f = open(index_file, 'r')
    for line in f:
        ticker = line.split("\t")[0]
        company_name = line.split("\t")[1].replace("'","''")
        if ticker.replace("&","N")+".csv" in files:
            print "Dumping daa for: "+ticker
            f2 = open(path+ticker.replace("&","N")+".csv",'r')
            records = f2.read().split("\n")
            for i in xrange(len(records)-2,0,-1):
                ohlc = records[i].split(",")
                cursor.execute("INSERT INTO OHLC (`sec_id`,`date`,`open`,`high`,`low`,`close`) VALUES"\
                            + "((select id from security where yahoo_ticker='"+ticker+"' and sec_name='"+company_name+"'),'"+ohlc[0]+"',"+ohlc[1]+","+ohlc[2]+","+ohlc[3]+","+ohlc[4]+")")
            f2.close()
        else:
            print "ERROR"
    f.close()
    conn.commit()
    conn.close()


populate_initial_data("S&P500", "Indexes/SNP500.tsv")
populate_initial_data("FTSE100", "Indexes/FTSE100.tsv")
populate_initial_data("NIFTY50", "Indexes/NIFTY50.tsv")