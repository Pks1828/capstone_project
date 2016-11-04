from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import json
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import base64


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
        ohlc_data = Ohlc.objects.filter(sec_id=stock_id).order_by("id")
        dates  = []
        openp  = []
        highp  = []
        lowp   = []
        closep = []
        ohlc   = []
        for d in ohlc_data:
            dates.append(d.date)
            openp.append(d.open)
            highp.append(d.high)
            lowp.append(d.low)
            closep.append(d.close)
            ohlc.append([d.date, d.open, d.high, d.low, d.close])
        dates  = dates[max(0,len(dates)-50+1):len(dates)]
        openp  = openp[max(0,len(dates)-50+1):len(dates)]
        highp  = highp[max(0,len(dates)-50+1):len(dates)]
        lowp   = lowp[max(0,len(dates)-50+1):len(dates)]
        closep = closep[max(0,len(dates)-50+1):len(dates)]
        fig, ax = plt.subplots()
        candlestick2_ohlc(ax, openp, highp, lowp, closep, width=0.6)
        # candlestick2_ohlc(ax, ohlc, width=0.6)
        fig.autofmt_xdate()
        fig.tight_layout()
        format = "png"
        sio = BytesIO()
        plt.savefig(sio, format=format)
        # context = {}
        context = {"ohlc_image":base64.b64encode(sio.getvalue())}
        return render(request, "StockAnalysis/report.html", context)



def make_chart():
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))