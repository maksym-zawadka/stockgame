from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import TodayDate
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as opy
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,DatetimeTickFormatter
from bokeh.embed import components
from django.core.cache import cache

def home(request):
    return render(request, 'home.html')


def analysis(request):
    # today date
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    daysInGame = 0
    defaultndays = 92
    defaultndaysSP = 63
    #pobranie zakresu i zachowanie w sesji
    if request.method == 'POST':
        buttonNDX=request.POST.get('saveTimeN')
        if buttonNDX == "1m":
            ndays=30
            request.session['daysNDX']=ndays
        elif buttonNDX == "3m":
            ndays=92
            request.session['daysNDX']=ndays
        elif buttonNDX == "6m":
            ndays = 183
            request.session['daysNDX']=ndays
        elif buttonNDX == "1y":
            ndays = 365
            request.session['daysNDX']=ndays
        elif buttonNDX == "5y":
            ndays = 1825
            request.session['daysNDX']=ndays
        buttonSP = request.POST.get('saveTimeS')
        if buttonSP == "1m":
            ndaysSP = 20
            request.session['daysSP']=ndaysSP
        elif buttonSP == "3m":
            ndaysSP = 60
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
        # chart
        # 1828 - ostatni dzien z przed rozpoczeciem

    #Zachowanie przedzialu czasu w zmiennej sesji
    ndays = request.session.get('daysNDX')
    if ndays is None:
        ndays = defaultndays

    ndaysSP = request.session.get('daysSP')
    if ndaysSP is None:
        ndaysSP = defaultndaysSP
    #NASDAQ 100
    df = pd.read_csv("Stocks/ndx.csv", sep=';', header=0, encoding='utf-8', nrows=ndays, skiprows=range(1,1828+daysInGame-ndays))

    # fig = go.Figure(
    #     data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
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
        years=["%d/%m/%Y"],)

    scriptN, divN = components(p)


    #SP500
    #1258
    dfS = pd.read_csv("Stocks/spx.csv", sep=';', header=0, encoding='utf-8', nrows=ndaysSP, skiprows=range(1,1259+daysInGame-ndaysSP))

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

    return render(request, 'analysis.html',
                  {'today': today, 'day': dayName, 'month': monthName, 'divN': divN, 'scriptN': scriptN, 'divS': divS, 'scriptS': scriptS})
