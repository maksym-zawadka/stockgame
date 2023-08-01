import ta.trend
from django.shortcuts import render
from .models import TodayDate, Stock, Money
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.embed import components
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


def analysis(request):
    # today date
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    daysInGame = todayObj.daysInGame
    defaultndays = 63
    defaultndaysSP = 63
    defaultndaysD = 63
    # pobranie zakresu i zachowanie w sesji
    if request.method == 'POST':
        buttonNDX = request.POST.get('saveTimeN')
        if buttonNDX == "1m":
            ndays = 21
            request.session['daysNDX'] = ndays
        elif buttonNDX == "3m":
            ndays = 63
            request.session['daysNDX'] = ndays
        elif buttonNDX == "6m":
            ndays = 126
            request.session['daysNDX'] = ndays
        elif buttonNDX == "1y":
            ndays = 240
            request.session['daysNDX'] = ndays
        elif buttonNDX == "5y":
            ndays = 1200
            request.session['daysNDX'] = ndays
        buttonSP = request.POST.get('saveTimeS')
        if buttonSP == "1m":
            ndaysSP = 21
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "3m":
            ndaysSP = 63
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "6m":
            ndaysSP = 126
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "1y":
            ndaysSP = 240
            request.session['daysSP'] = ndaysSP
        elif buttonSP == "5y":
            ndaysSP = 1200
            request.session['daysSP'] = ndaysSP
        buttonD = request.POST.get('saveTimeD')
        if buttonD == "1m":
            ndaysD = 21
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
            request.session['ticker'] = request.POST.get('ticker')

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
    df = pd.read_csv("Stocks/ndx.us.csv", sep=',', header=0, encoding='utf-8', nrows=1258 + daysInGame)
    ndxEMA = ta.trend.EMAIndicator(close=df['Close'], window=30, fillna=False)
    ndxSMA = ta.trend.SMAIndicator(close=df['Close'], window=30, fillna=False)
    df['EMA'] = ndxEMA.ema_indicator()
    df['SMA'] = ndxSMA.sma_indicator()
    df = df.drop(df.index[0:1258 + daysInGame - ndays])
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
    # p.line(df.Date, df.EMA, line_color="orange", line_width=1.5)
    # p.line(df.Date, df.SMA, line_color="purple", line_width=1.5)
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
    dfS = pd.read_csv("Stocks/spx.us.csv", sep=',', header=0, encoding='utf-8', nrows=ndaysSP,
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

    divD = ""
    scriptD = ""

    # ADVANCED SEARCH
    ticker = request.session.get('ticker')
    if ticker is None:
        ticker = ""
    if ticker:
        # SMA10
        buttonSMA10 = request.POST.get('SMA10')
        if buttonSMA10 is None:
            request.session['sma10'] = 0
        else:
            request.session['sma10'] = 10
        # SMA20
        buttonSMA20 = request.POST.get('SMA20')
        if buttonSMA20 is None:
            request.session['sma20'] = 0
        else:
            request.session['sma20'] = 20
        # SMA50
        buttonSMA50 = request.POST.get('SMA50')
        if buttonSMA50 is None:
            request.session['sma50'] = 0
        else:
            request.session['sma50'] = 50
        # SMA100
        buttonSMA100 = request.POST.get('SMA100')
        if buttonSMA100 is None:
            request.session['sma100'] = 0
        else:
            request.session['sma100'] = 100
        # SMA200
        buttonSMA200 = request.POST.get('SMA200')
        if buttonSMA200 is None:
            request.session['sma200'] = 0
        else:
            request.session['sma200'] = 200

        # EMA10
        buttonEMA10 = request.POST.get('EMA10')
        if buttonEMA10 is None:
            request.session['ema10'] = 0
        else:
            request.session['ema10'] = 10
        # EMA20
        buttonEMA20 = request.POST.get('EMA20')
        if buttonEMA20 is None:
            request.session['ema20'] = 0
        else:
            request.session['ema20'] = 20
        # EMA50
        buttonEMA50 = request.POST.get('EMA50')
        if buttonEMA50 is None:
            request.session['ema50'] = 0
        else:
            request.session['ema50'] = 50
        # EMA100
        buttonEMA100 = request.POST.get('EMA100')
        if buttonEMA100 is None:
            request.session['ema100'] = 0
        else:
            request.session['ema100'] = 100
        # EMA200
        buttonEMA200 = request.POST.get('EMA200')
        if buttonEMA200 is None:
            request.session['ema200'] = 0
        else:
            request.session['ema200'] = 200

        # szukanie ktora z kolei jest linia z dzisiejsza data
        date = today.strftime("%Y-%m-%d")
        linenum = 0
        f = open("Stocks/" + ticker + ".us.csv")
        for nr_linii, linia in enumerate(f, start=1):
            if linia.startswith(date):
                linenum = nr_linii
        # max period
        if ndaysD == 1200:
            ndaysD = linenum - 1
        data = pd.read_csv("Stocks/" + ticker + ".us.csv", sep=',', header=0, encoding='utf-8',
                           nrows=linenum - 1 + daysInGame)

        # DODAWANIE KOLUMN Z SMA
        if request.session.get('sma10') != 0:
            dSMA = ta.trend.SMAIndicator(close=data['Close'], window=10, fillna=False)
            data['SMA10'] = dSMA.sma_indicator()
        if request.session.get('sma20') != 0:
            dSMA = ta.trend.SMAIndicator(close=data['Close'], window=20, fillna=False)
            data['SMA20'] = dSMA.sma_indicator()
        if request.session.get('sma50') != 0:
            dSMA = ta.trend.SMAIndicator(close=data['Close'], window=50, fillna=False)
            data['SMA50'] = dSMA.sma_indicator()
        if request.session.get('sma100') != 0:
            dSMA = ta.trend.SMAIndicator(close=data['Close'], window=100, fillna=False)
            data['SMA100'] = dSMA.sma_indicator()
        if request.session.get('sma200') != 0:
            dSMA = ta.trend.SMAIndicator(close=data['Close'], window=200, fillna=False)
            data['SMA200'] = dSMA.sma_indicator()

        # DODAWANIE KOLUMN Z EMA
        if request.session.get('ema10') != 0:
            dEMA = ta.trend.EMAIndicator(close=data['Close'], window=10, fillna=False)
            data['EMA10'] = dEMA.ema_indicator()
        if request.session.get('ema20') != 0:
            dEMA = ta.trend.EMAIndicator(close=data['Close'], window=20, fillna=False)
            data['EMA20'] = dEMA.ema_indicator()
        if request.session.get('ema0') != 0:
            dEMA = ta.trend.EMAIndicator(close=data['Close'], window=50, fillna=False)
            data['EMA50'] = dEMA.ema_indicator()
        if request.session.get('ema100') != 0:
            dEMA = ta.trend.EMAIndicator(close=data['Close'], window=100, fillna=False)
            data['EMA100'] = dEMA.ema_indicator()
        if request.session.get('ema200') != 0:
            dEMA = ta.trend.EMAIndicator(close=data['Close'], window=200, fillna=False)
            data['EMA200'] = dEMA.ema_indicator()

        # usuniecie danych spoza wyznaczonego  zakresu
        data = data.drop(data.index[0:linenum - 1 + daysInGame - ndaysD])
        data['Date'] = pd.to_datetime(data['Date'])
        sourceData = ColumnDataSource(data)

        incData = data.Close > data.Open
        decData = data.Open > data.Close
        w = 12 * 60 * 60 * 1000  # half day in ms
        # Tworzenie wykresu świecowego
        pData = figure(x_axis_type='datetime', title=ticker, width=1200, height=600, sizing_mode="fixed", tools="")
        pData.segment(x0='Date', y0='High', x1='Date', y1='Low', source=sourceData, color="black")
        pData.vbar(data.Date[incData], w, data.Open[incData], data.Close[incData], fill_color="green",
                   line_color="black")
        pData.vbar(data.Date[decData], w, data.Open[decData], data.Close[decData], fill_color="red", line_color="black")

        # RYSOWANIE SMA
        if request.session.get('sma10') != 0:
            pData.line(data.Date, data.SMA10, line_color="blue", line_width=2.0, legend_label="SMA10")
        if request.session.get('sma20') != 0:
            pData.line(data.Date, data.SMA20, line_color="cyan", line_width=2.0, legend_label="SMA20")
        if request.session.get('sma50') != 0:
            pData.line(data.Date, data.SMA50, line_color="#FF007F", line_width=2.0, legend_label="SMA50")
        if request.session.get('sma100') != 0:
            pData.line(data.Date, data.SMA100, line_color="#F88A38", line_width=2.0, legend_label="SMA100")
        if request.session.get('sma200') != 0:
            pData.line(data.Date, data.SMA200, line_color="#39FF14", line_width=2.0, legend_label="SMA200")
        # RYSOWANIE EMA
        if request.session.get('ema10') != 0:
            pData.line(data.Date, data.EMA10, line_dash="dashed", line_color="blue", line_width=2.0,
                       legend_label="EMA10")
        if request.session.get('ema20') != 0:
            pData.line(data.Date, data.EMA20, line_dash="dashed", line_color="cyan", line_width=2.0,
                       legend_label="EMA20")
        if request.session.get('ema50') != 0:
            pData.line(data.Date, data.EMA50, line_dash="dashed", line_color="#FF007F", line_width=2.0,
                       legend_label="EMA50")
        if request.session.get('ema100') != 0:
            pData.line(data.Date, data.EMA100, line_dash="dashed", line_color="#F88A38", line_width=2.0,
                       legend_label="EMA100")
        if request.session.get('ema200') != 0:
            pData.line(data.Date, data.EMA200, line_dash="dashed", line_color="#39FF14", line_width=2.0,
                       legend_label="EMA200")

        pData.toolbar.logo = None
        pData.border_fill_color = None
        pData.title.text_font_size = '16pt'
        pData.xaxis.formatter = DatetimeTickFormatter(
            days=["%d/%m/%Y"],
            months=["%d/%m/%Y"],
            years=["%d/%m/%Y"], )
        # legend
        pData.legend.location = "top_left"
        pData.legend.title = "Indicators"

        scriptD, divD = components(pData)

    return render(request, 'analysis.html',
                  {'today': today, 'day': dayName, 'month': monthName, 'divN': divN, 'scriptN': scriptN, 'divS': divS,
                   'scriptS': scriptS, 'divD': divD, 'scriptD': scriptD, 'ticker': ticker})


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
