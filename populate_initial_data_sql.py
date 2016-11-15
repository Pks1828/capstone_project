import mysql.connector
from CapstoneProject.settings import DATABASES
import os


def populate_initial_data(index_name, index_file):
    global counter
    global base_query
    global out
    path = "stock_data/"+index_name.replace("&","N")+"/"
    files = os.listdir(path)
    f = open(index_file, 'r')
    for line in f:
        ticker = line.split("\t")[0].strip().replace("\n","")
        company_name = line.split("\t")[1].replace("'","''").strip().replace("\n","")
        if ticker.replace("&","N")+".csv" in files:
            print "Dumping daa for: "+ticker
            f2 = open(path+ticker.replace("&","N")+".csv",'r')
            records = f2.read().split("\n")
            for i in xrange(len(records)-1,0,-1):
                ohlc = records[i].split(",")
                try:
                    if len(ohlc)<5:
                        continue
                    if counter==0:
                        q = "((select id from security where yahoo_ticker='"+ticker+"' and sec_name='"+company_name+"'),'"+ohlc[0]+"',"+ohlc[1]+","+ohlc[2]+","+ohlc[3]+","+ohlc[4]+")"
                        counter+=1
                    else:
                        q = ",((select id from security where yahoo_ticker='"+ticker+"' and sec_name='"+company_name+"'),'"+ohlc[0]+"',"+ohlc[1]+","+ohlc[2]+","+ohlc[3]+","+ohlc[4]+")"
                        counter+=1
                    if counter>=25000:
                        out.write(q+";\n")
                        out.write(base_query+"\n")
                        # print(q+";")
                        # print(base_query)
                        counter=0
                    else:
                        # print (q)
                        out.write(q+"\n")
                except:
                    print "ERROR"
            f2.close()
        else:
            print "ERROR"
    f.close()

counter = 0
base_query = "INSERT INTO OHLC (`sec_id`,`date`,`open`,`high`,`low`,`close`) VALUES "
out = open("queries_ohlc.sql", 'w')
out.write(base_query+"\n")
populate_initial_data("S&P500", "Indexes/SNP500.tsv")
populate_initial_data("FTSE100", "Indexes/FTSE100.tsv")
populate_initial_data("NIFTY50", "Indexes/NIFTY50.tsv")
out.close()
