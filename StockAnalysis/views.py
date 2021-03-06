from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import json
import math
from .technical_indicators import TechnicalIndicators, TechnicalAnalysis
from .stock_data import StockData
import numpy as np
from CapstoneProject.settings import BASE_DIR
from django.db.models import Min, Max


def index(request):
    context = {"title":"Home"}
    return render(request, "StockAnalysis/index.html", context)


def search(request):
    if request.method == "GET":
        context = {"title":"Search"}
        context["indexes"] = Indexes.objects.all()
        return render(request, "StockAnalysis/search.html", context)


def search_stocks(request):
    if request.method=="GET":
        return redirect("/search")
    else:
        index_id = request.POST['index_id']
        stock_names = Constituents.objects.filter(index_id__exact=index_id)
        result = []
        for stock_name in stock_names:
            result.append({"id":stock_name.sec_id, "sec_name":stock_name.sec.sec_name})
        return HttpResponse(json.dumps({"stock_names":result}), content_type='application/json')


def report(request):
    if request.method=="GET":
        return redirect("/search")
    else:
        stock_id = request.POST['select_stock']
        ohlc_data = Ohlc.objects.all().filter(sec_id=stock_id).order_by("date")
        dates  = []
        openp  = []
        highp  = []
        lowp   = []
        closep = []
        ohlc   = []
        ohlc_only = []
        for d in ohlc_data:
            dates.append(d.date)
            openp.append(d.open)
            highp.append(d.high)
            lowp.append(d.low)
            closep.append(d.close)
            ohlc.append([d.date, d.open, d.high, d.low, d.close])
            ohlc_only.append([d.open, d.high, d.low, d.close])
        try:
            stock_data = StockData(dates, openp, highp, lowp, closep)
        except:
            return render(request, "StockAnalysis/index.html", {"title":"Home", "error":"Number of datapoints are less than 200 for the analysis."})
        technical_indicators = TechnicalIndicators(stock_data)
        technical_indicators.calculate_with_defaults()
        technical_analysis = TechnicalAnalysis(technical_indicators, stock_data)
        technical_analysis.get_all_signals()
        technical_analysis.calculate_weights()
        reco = technical_analysis.give_recommendation()
        indicators = technical_analysis.get_indicators()
        openp  = openp[max(0,len(dates)-50):len(dates)]
        highp  = highp[max(0,len(dates)-50):len(dates)]
        lowp   = lowp[max(0,len(dates)-50):len(dates)]
        closep = closep[max(0,len(dates)-50):len(dates)]
        dates  = dates[max(0,len(dates)-50):len(dates)]
        # sio = make_chart("Equity", dates, openp, highp, lowp, closep)
        # context = {"ohlc_image":base64.b64encode(sio.getvalue())}
        rising_sticks = []
        falling_sticks = []
        for i in range(len(dates)):
            if closep[i]>openp[i]:
                rising_sticks.append([dates[i],[openp[i], highp[i], lowp[i], closep[i]]])
            else:
                falling_sticks.append([dates[i],[openp[i], highp[i], lowp[i], closep[i]]])
        stock_name = Security.objects.filter(id=stock_id).values_list('sec_name', flat=True)[0].replace("\n","")
        text = stock_name+" is recommended for a \""+reco+"\" at "+str(closep[-1])+"."
        if reco=="BUY":
            text += " The expected profit and loss levels are "+str(closep[-1]+2.0*np.std(closep))+", "+str(closep[-1]-2.0*np.std(closep))+" respectively."
        elif reco=="SELL":
            text += " The expected profit and loss levels are "+str(closep[-1]-2.0*np.std(closep))+", "+str(closep[-1]+2.0*np.std(closep))+" respectively."
        context = {"chart_title":"TITLE", "rising_sticks":rising_sticks, "falling_sticks": falling_sticks, "recommendation":reco, "stock_name":stock_name\
            , "indicators":indicators, "text":text}
        return render(request, "StockAnalysis/report.html", context)


def glossary(request):
    return render(request, "StockAnalysis/glossary.html")


def performance(request):
    file_names = ["AAPL_p.csv","KO_p.csv","GE_p.csv","HPQ_p.csv","MSFT_p.csv"];
    context = {}
    for file in file_names:
        f = open(BASE_DIR+"/performance/"+file,'r')
        records = f.read().split("\n")
        numReco = []
        data = []
        for record in records:
            if record=="":
                continue
            n,d = record.split(",")
            n = int(n)
            d = float(d)
            numReco.append(n)
            data.append(d)
        if file=="AAPL_p.csv":
            context['data1'] = zip(numReco,data)
        elif file=="KO_p.csv":
            context['data2'] = zip(numReco,data)
        elif file=="GE_p.csv":
            context['data3'] = zip(numReco,data)
        elif file=="HPQ_p.csv":
            context['data4'] = zip(numReco,data)
        elif file=="MSFT_p.csv":
            context['data5'] = zip(numReco,data)
        f.close()
    return render(request,'StockAnalysis/performance.html',context)


def top_picks(request):
    max_date = list(TopPicks.objects.aggregate(Max('date')).values())
    if len(max_date)>0:
        max_date = max_date[0]
    else:
        context = {"title":"Home", "error":"No top picks found!"}
        return render(request,  "StockAnalysis/index.html", context)
    data_list = TopPicks.objects.filter(date=max_date).order_by("id")
    result = []
    for data in data_list:
        reco = "NEUTRAL"
        if data.score>0:
            reco="BUY"
        elif data.score<0:
            reco="SELL"
        result.append({"sec_id":data.sec_id, "reco":reco, "name":data.sec.sec_name})
    context = {"top_picks":result}
    return render(request, "StockAnalysis/top_picks.html",context)