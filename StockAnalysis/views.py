from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import json
from matplotlib.finance import candlestick2_ohlc
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import matplotlib.dates as mdates
import base64
from matplotlib.dates import date2num
import matplotlib.ticker as mticker

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
        sio = make_chart("Equity", dates, openp, highp, lowp, closep)
        context = {"ohlc_image":base64.b64encode(sio.getvalue())}
        return render(request, "StockAnalysis/report.html", context)


def make_chart(title, dates, openp, highp, lowp, closep):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    ohlc = []
    for i in range(len(dates)):
        ohlc.append((date2num(dates[i]), openp[i], highp[i], lowp[i], closep[i]))
    # candlestick2_ohlc(ax1, openp, highp, lowp, closep, width=0.4, colorup='#77d879', colordown='#db3f3f')
    print("DATES:"+str(dates[-1]))
    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)


    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(title)
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    sio = BytesIO()
    plt.savefig(sio, format="png")
    return sio
