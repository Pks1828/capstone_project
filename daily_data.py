import urllib
import datetime
import time
import mysql.connector
import os
from CapstoneProject.settings import DATABASES
from StockAnalysis.technical_indicators import TechnicalAnalysis, TechnicalIndicators
from StockAnalysis.stock_data import StockData
import operator


def get_url(ticker, start_day, start_month, start_year, end_day, end_month, end_year):
    # http://chart.finance.yahoo.com/table.csv?s=YHOO&a=9&b=15&c=2016&d=10&e=15&f=2016&g=d&ignore=.csv
    # http://chart.finance.yahoo.com/table.csv?s=IHG&a=10&b=15&c=2016&d=9&e=15&f=2016&g=d&ignore=.csv
    base_url = "http://chart.finance.yahoo.com/table.csv?s=TICKER&a=START_MONTH&b=START_DAY&c=START_YEAR&d=END_MONTH&e=END_DAY&f=END_YEAR&g=d&ignore=.csv"
    return base_url.replace("TICKER",ticker).replace("START_DAY",str(start_day)).replace("START_MONTH",str(start_month-1)).replace("START_YEAR",str(start_year))\
            .replace("END_DAY",str(end_day)).replace("END_MONTH",str(end_month-1)).replace("END_YEAR",str(end_year))


def download_file(url, filepath):
    '''
    Downloads the file from the given url
    Args:
        filepath: The Absolute or Relative path of file including filename and extension
        url: The url from which we need to download the data

    Returns:

    '''
    urllib.urlretrieve (url.replace("\\","/"), filepath)


def daily_download():
    conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
    cursor = conn.cursor()
    cursor.execute("SELECT id, yahoo_ticker from security")
    stock_data = cursor.fetchall()
    d = datetime.datetime.now()
    for data in stock_data:
        sec_id = str(data[0])
        ticker = data[1]
        url = get_url(ticker, d.day, d.month-1, d.year, d.day, d.month, d.year)
        try:
            download_file(url, "table.csv")
            f = open("table.csv",'r')
            records = f.read().split("\n")
            for i in range(1,len(records)):
                if records[i].strip()=="":
                    continue
                ohlcd = records[i].split(",")
                if len(ohlcd)<5:
                    continue
                date_val = ohlcd[0]
                openp = ohlcd[1]
                highp = ohlcd[2]
                lowp = ohlcd[3]
                closep = ohlcd[4]
                cursor.execute("select 1 from ohlc where sec_id="+sec_id+" and `date`='"+date_val+"'")
                check_record = cursor.fetchall()
                if check_record and len(check_record)>0:
                    break
                q = "INSERT INTO ohlc (`date`,`open`,`high`,`low`,`close`) values ('"+date_val+"',"+openp+","+highp+","+lowp+","+closep+")"
                cursor.execute(q)
        except Exception as e:
            f.close()
            print ("ERROR: "+str(e)+":"+url)
        conn.commit()
        f.close()
    cursor.close()
    conn.close()


class StockScore:
    def __init__(self, sec_id, score):
        self.sec_id = sec_id
        self.score = score
        self.abs_score = abs(score)

    def __str__(self):
        return "{SecID: "+str(self.sec_id)+", Score: "+str(self.score)+", AbsScore: "+str(self.abs_score)+"}"


def technical_analysis():
    conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
    cursor = conn.cursor()
    cursor.execute("select max(date) from ohlc")
    max_date = cursor.fetchall()[0][0]
    cursor.execute("select 1 from top_picks where `date`='"+str(max_date)+"'")
    check_today = cursor.fetchall()
    if check_today and len(check_today)>0:
        print ("Todays analysis is already Done")
        cursor.close()
        conn.close()
        return
    cursor.execute("SELECT id, yahoo_ticker from security")
    stock_data = cursor.fetchall()
    score_data = []
    for data in stock_data:
        sec_id = str(data[0])
        ticker = data[1]
        print("Current : "+ticker)
        cursor.execute("SELECT `date`, `open`, `high`, `low`, `close` from ohlc where sec_id="+sec_id+" order by `date` DESC limit 200")
        records = cursor.fetchall()
        i = len(records)-1
        try:
            dates = []
            openp = []
            highp = []
            lowp = []
            closep = []
            while i>=0:
                dates.append(records[i][0])
                openp.append(records[i][1])
                highp.append(records[i][2])
                lowp.append(records[i][3])
                closep.append(records[i][4])
                i-=1
            stock_data = StockData(dates, openp, highp, lowp, closep)
            technical_indicators = TechnicalIndicators(stock_data)
            technical_indicators.calculate_with_defaults()
            technical_analysis = TechnicalAnalysis(technical_indicators, stock_data)
            technical_analysis.get_all_signals()
            technical_analysis.calculate_weights()
            score = technical_analysis.get_score()
            score_data.append(StockScore(sec_id, score))
        except Exception as e:
            print ("ERROR! : "+str(e))
    score_data.sort(key=operator.attrgetter('abs_score'), reverse=True)
    for i in range(min(10,len(score_data))):
        q = "INSERT INTO top_picks (`date`,sec_id,`score`) VALUES ('"+str(max_date)+"',"+str(score_data[i].sec_id)+","+str(score_data[i].score)+")"
        cursor.execute(q)
    conn.commit()
    cursor.close()
    conn.close()

daily_download()
technical_analysis()