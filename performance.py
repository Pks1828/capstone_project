from StockAnalysis.technical_indicators import TechnicalIndicators, TechnicalAnalysis, carryover
from StockAnalysis.stock_data import StockData
import mysql.connector
from CapstoneProject.settings import DATABASES
import math
import numpy as np

# +-----------------------+--------------+
# | The Coca Cola Company | KO           |
# | General Electric      | GE           |
# | HP Inc.               | HPQ          |
# | Apple Inc.            | APPL         |
# | Microsoft Corp.       | MSFT         |
# +-----------------------+--------------+
#

sec_id = [148, 217, 308, 335, 407]
# sec_id = [148]
names = ['Apple Inc.','The Coca Cola Company','General Electric','HP Inc.','Microsoft Corp.']
yahoo_ticker = ['AAPL','KO','GE','HPQ','MSFT']


conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
cursor = conn.cursor()


for i in range(len(sec_id)):
    q = "Select `date`, `open`, `high`, `low`, `close` from ohlc where sec_id="+str(sec_id[i])+" order by `date`"
    cursor.execute(q)
    results = cursor.fetchall()
    dates = []
    openp = []
    highp = []
    lowp = []
    closep = []
    # skip = 8550
    for result in results:
        # if skip>0:
        #     skip-=1
        #     continue
        dates.append(result[0])
        openp.append(result[1])
        highp.append(result[2])
        lowp.append(result[3])
        closep.append(result[4])
    print ("Total Iterations: "+str(len(dates)-200))
    reco = []
    for j in range(200,len(dates)):
        print ("Iteration: "+str(j-200))
        c_dates = dates[j-200:j]
        c_openp = openp[j-200:j]
        c_highp = highp[j-200:j]
        c_lowp = lowp[j-200:j]
        c_closep = closep[j-200:j]
        stock_data = StockData(c_dates, c_openp, c_highp, c_lowp, c_closep, -1)
        ti = TechnicalIndicators(stock_data)
        ti.calculate_with_defaults()
        ta = TechnicalAnalysis(ti, stock_data)
        ta.get_all_signals()
        ta.calculate_weights()
        reco_str = ta.give_recommendation()
        if reco_str=="BUY":
            reco.append(1)
        elif reco_str=="SELL":
            reco.append(-1)
        else:
            reco.append(0)
    reco = [0 for k in range(200)]+carryover(reco, -1)
    ret = []
    j = 200
    returns = 0
    while j < len(dates):
        if reco[j]>0:
            c_reco = 1
            target = closep[j]+2*np.std(closep[j-50:j])*math.sqrt(10)
            stoploss = max(closep[j]-2*np.std(closep[j-50:j])*math.sqrt(10),0)
        else:
            c_reco = -1
            stoploss = closep[j]+2*np.std(closep[j-50:j])*math.sqrt(10)
            target = max(closep[j]-2*np.std(closep[j-50:j])*math.sqrt(10),0)
        reco_price = closep[j]
        j+=1
        count = 0
        reco_made = False
        while j<len(dates) and count<20 and reco[j]==c_reco:
            if c_reco>0:
                if highp[j]>=target:
                    returns += highp[j]-target
                    ret.append(returns)
                    reco_made = True
                    break
                elif lowp[j]<=stoploss:
                    returns += lowp[j]-stoploss
                    ret.append(returns)
                    reco_made = True
                    break
            else:
                if highp[j]>=stoploss:
                    returns += stoploss-highp[j]
                    ret.append(returns)
                    reco_made = True
                    break
                elif lowp[j]<=target:
                    returns += target-lowp[j]
                    ret.append(returns)
                    reco_made = True
                    break
            count +=1
            j+=1
        if reco_made:
            j+=1
        else:
            returns += closep[j-1] - reco_price
            ret.append(returns)
    f_o = open("performance/"+yahoo_ticker[i]+"_p.csv",'w')
    for r in range(len(ret)):
        f_o.write(str(r+1)+","+str(ret[r])+"\n")
    f_o.close()
cursor.close()
conn.close()