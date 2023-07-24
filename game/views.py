from django.shortcuts import render
from .models import TodayDate, Stock, Money
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.embed import components
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def home(request):
    return render(request, 'home.html')


def analysis(request):
    # today date
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    daysInGame = todayObj.daysInGame
    defaultndays = 92
    defaultndaysSP = 63
    defaultndaysD=63
    # pobranie zakresu i zachowanie w sesji
    if request.method == 'POST':
        buttonNDX = request.POST.get('saveTimeN')
        if buttonNDX == "1m":
            ndays = 30
            request.session['daysNDX'] = ndays
        elif buttonNDX == "3m":
            ndays = 92
            request.session['daysNDX'] = ndays
        elif buttonNDX == "6m":
            ndays = 183
            request.session['daysNDX'] = ndays
        elif buttonNDX == "1y":
            ndays = 365
            request.session['daysNDX'] = ndays
        elif buttonNDX == "5y":
            ndays = 1825
            request.session['daysNDX'] = ndays
        buttonSP = request.POST.get('saveTimeS')
        if buttonSP == "1m":
            ndaysSP = 20
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "3m":
            ndaysSP = 63
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "6m":
            ndaysSP = 120
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "1y":
            ndaysSP = 240
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "5y":
            ndaysSP = 1200
            request.session['daysSP'] = ndaysSP
        buttonD = request.POST.get('saveTimeD')
        if buttonD == "1m":
            ndaysD= 20
            request.session['daysD'] = ndaysD
        elif buttonD == "3m":
            ndaysD = 63
            request.session['daysD'] = ndaysD
        elif buttonD == "6m":
            ndaysD = 120
            request.session['daysD'] = ndaysD
        elif buttonD == "1y":
            ndaysD = 240
            request.session['daysD'] = ndaysD
        elif buttonD == "max":
            ndaysD = 1200
            request.session['daysD'] = ndaysD
        if 'search_button' in request.POST:
             request.session['ticker']= request.POST.get('ticker')

        # chart
        # 1828 - ostatni dzien z przed rozpoczeciem

    # Zachowanie przedzialu czasu w zmiennej sesji
    ndays = request.session.get('daysNDX')
    if ndays is None:
        ndays = defaultndays

    ndaysSP = request.session.get('daysSP')
    if ndaysSP is None:
        ndaysSP = defaultndaysSP

    ndaysD = request.session.get('daysD')
    if ndaysD is None:
        ndaysD = defaultndaysD
    # NASDAQ 100
    df = pd.read_csv("Stocks/ndx.csv", sep=';', header=0, encoding='utf-8', nrows=ndays,
                     skiprows=range(1, 1828 + daysInGame - ndays))

    df['Date'] = pd.to_datetime(df['Date'])
    source = ColumnDataSource(df)

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12 * 60 * 60 * 1000  # half day in ms
    # Tworzenie wykresu świecowego
    p = figure(x_axis_type='datetime', title='Nasdaq 100 (^NDX)', width=800, height=400, sizing_mode="fixed", tools="")
    p.segment(x0='Date', y0='High', x1='Date', y1='Low', source=source, color="black")
    p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="green", line_color="black")
    p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="red", line_color="black")
    p.toolbar.logo = None
    p.border_fill_color = None
    p.title.text_font_size = '16pt'
    p.xaxis.formatter = DatetimeTickFormatter(
        days=["%d/%m/%Y"],
        months=["%d/%m/%Y"],
        years=["%d/%m/%Y"], )

    scriptN, divN = components(p)

    # SP500
    # 1258
    dfS = pd.read_csv("Stocks/spx.csv", sep=';', header=0, encoding='utf-8', nrows=ndaysSP,
                      skiprows=range(1, 1259 + daysInGame - ndaysSP))

    dfS['Date'] = pd.to_datetime(dfS['Date'])
    sourceS = ColumnDataSource(dfS)

    incS = dfS.Close > dfS.Open
    decS = dfS.Open > dfS.Close
    w = 12 * 60 * 60 * 1000  # half day in ms
    # Tworzenie wykresu świecowego
    pS = figure(x_axis_type='datetime', title='S&P 500 (^SPX)', width=800, height=400, sizing_mode="fixed", tools="")
    pS.segment(x0='Date', y0='High', x1='Date', y1='Low', source=sourceS, color="black")
    pS.vbar(dfS.Date[incS], w, dfS.Open[incS], dfS.Close[incS], fill_color="green", line_color="black")
    pS.vbar(dfS.Date[decS], w, dfS.Open[decS], dfS.Close[decS], fill_color="red", line_color="black")
    pS.toolbar.logo = None
    pS.border_fill_color = None
    pS.title.text_font_size = '16pt'
    pS.xaxis.formatter = DatetimeTickFormatter(
        days=["%d/%m/%Y"],
        months=["%d/%m/%Y"],
        years=["%d/%m/%Y"], )

    scriptS, divS = components(pS)

    divD=""
    scriptD=""

    # WYSZUKIWANIE
    ticker = request.session.get('ticker')
    if ticker is None:
        ticker = ""
    if ticker:
        #szukanie ktora z kolei jest linia z dzisiejsza data
        date=today.strftime("%Y-%m-%d")
        linenum=0
        f = open("Stocks/" + ticker + ".us.csv")
        for nr_linii, linia in enumerate(f, start=1):
            if linia.startswith(date):
                linenum=nr_linii
        if ndaysD==1200:
            ndaysD=linenum-1
        data = pd.read_csv("Stocks/" + ticker + ".us.csv", sep=',', header=0, encoding='utf-8', nrows=ndaysD, skiprows=range(1, linenum-1 - ndaysD))
        data['Date'] = pd.to_datetime(data['Date'])
        sourceData = ColumnDataSource(data)

        incData = data.Close > data.Open
        decData = data.Open > data.Close
        w = 12 * 60 * 60 * 1000  # half day in ms
        # Tworzenie wykresu świecowego
        pData = figure(x_axis_type='datetime', title=ticker, width=800, height=400, sizing_mode="fixed", tools="")
        pData.segment(x0='Date', y0='High', x1='Date', y1='Low', source=sourceData, color="black")
        pData.vbar(data.Date[incData], w, data.Open[incData], data.Close[incData], fill_color="green", line_color="black")
        pData.vbar(data.Date[decData], w, data.Open[decData], data.Close[decData], fill_color="red", line_color="black")
        pData.toolbar.logo = None
        pData.border_fill_color = None
        pData.title.text_font_size = '16pt'
        pData.xaxis.formatter = DatetimeTickFormatter(
            days=["%d/%m/%Y"],
            months=["%d/%m/%Y"],
            years=["%d/%m/%Y"], )

        scriptD, divD = components(pData)

    return render(request, 'analysis.html',
                  {'today': today, 'day': dayName, 'month': monthName, 'divN': divN, 'scriptN': scriptN, 'divS': divS,
                   'scriptS': scriptS, 'divD': divD, 'scriptD': scriptD})


def portfolio(request):
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    # if request.method == 'POST':
    #     a = 0
    # else:
    #     ticker = Stock.objects.all()
    #     output = []
    #     labels = []
    #     data = []
    #     for ticker_item in ticker:

    return render(request, 'portfolio.html', {'today': today, 'day': dayName, 'month': monthName})

def dopasowania(request):
    wprowadzony_tekst = request.GET.get('q', '').lower()
    dopasowania_list = []
    f = open("Stocks/tickers.txt", 'r')
    linie = f.readlines()
    if linie:
        for linia in linie:
            dopasowania_list.append(linia.strip())


    dopasowania_list = [dopasowanie for dopasowanie in dopasowania_list if wprowadzony_tekst in dopasowanie.lower()]

    return JsonResponse(dopasowania_list, safe=False)