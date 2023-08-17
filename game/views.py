import ta.trend
import ta.volatility
from django.shortcuts import render, redirect
from .models import TodayDate, Stock, Money
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.embed import components
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta

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
    df = pd.read_csv("Stocks/ndx.us.csv", sep=',', header=0, encoding='utf-8', nrows=1259 + daysInGame)
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
    p = figure(x_axis_type='datetime', title='Nasdaq 100 (^NDX)', width=600, height=300, sizing_mode="fixed", tools="")
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
                      skiprows=range(1, 1260 + daysInGame - ndaysSP))

    dfS['Date'] = pd.to_datetime(dfS['Date'])
    sourceS = ColumnDataSource(dfS)

    incS = dfS.Close > dfS.Open
    decS = dfS.Open > dfS.Close
    w = 12 * 60 * 60 * 1000  # half day in ms
    # Tworzenie wykresu świecowego
    pS = figure(x_axis_type='datetime', title='S&P 500 (^SPX)', width=600, height=300, sizing_mode="fixed", tools="")
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
    scriptMACD = ""
    divMACD = ""
    # TICKER LIST
    lines = []
    with open("Stocks/tickers.txt", 'r') as file:
        for line in file:
            lines.append(line.strip())

    # ADVANCED SEARCH
    ticker = request.session.get('ticker')
    if ticker is None:
        ticker = ""
    elif ticker in lines:
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
        # MACD
        buttonMACD = request.POST.get('MACD')
        if buttonMACD is None:
            request.session['macd'] = 0
        else:
            request.session['macd'] = 1
        # BOLLINGER
        buttonBollinger = request.POST.get('BOLLINGER')
        if buttonBollinger is None:
            request.session['bollinger'] = 0
        else:
            request.session['bollinger'] = 1
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
                           nrows=linenum -1) #data wczorajsza wiec -2 bo liczone od zera

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

        # DODAWANIE KOLUMNY MACD
        if request.session.get('macd') == 1:
            dMACD = ta.trend.MACD(close=data['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=False)
            data['MACD'] = dMACD.macd()
            data['signalMACD'] = dMACD.macd_signal()
            data['histogramMACD'] = dMACD.macd_diff()

        # DODAWANIE KOLUMNY BOLLINGER
        if request.session.get('bollinger') == 1:
            dBOLLINGER = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2, fillna=False)
            data['BOLLINGERHBAND'] = dBOLLINGER.bollinger_hband()
            data['BOLLINGERLBAND'] = dBOLLINGER.bollinger_lband()
            data['BOLLINGERMAVG'] = dBOLLINGER.bollinger_mavg()

        # usuniecie danych spoza wyznaczonego  zakresu
        data = data.drop(data.index[0:linenum - 1 - ndaysD])
        data['Date'] = pd.to_datetime(data['Date'])
        sourceData = ColumnDataSource(data)
        sourceDataMACD = ColumnDataSource(data)
        incData = data.Close > data.Open
        decData = data.Open > data.Close
        w = 12 * 60 * 60 * 1000  # half day in ms
        # Tworzenie wykresu świecowego
        pData = figure(x_axis_type='datetime', title=ticker, width=900, height=500, sizing_mode="fixed", tools="")
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
        # RYSOWANIE BOLLINGER
        if request.session.get('bollinger') != 0:
            pData.line(data.Date, data.BOLLINGERHBAND, line_color="#b2badb", line_width=2.0,
                       legend_label="BB(20,2)")
            pData.line(data.Date, data.BOLLINGERLBAND, line_color="#b2badb", line_width=2.0)
            pData.line(data.Date, data.BOLLINGERMAVG, line_dash="dashed", line_color="#b2badb", line_width=2.0)

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

        # MACD CHART
        if request.session.get('macd') == 1:
            macdChart = figure(x_axis_type='datetime', width=900, height=250, sizing_mode="fixed",
                               tools="")
            macdChart.segment(x0='Date', source=sourceDataMACD)
            macdChart.line(data.Date, data.MACD, line_color="#C451EC", line_width=2.0,
                           legend_label="MACD")
            macdChart.line(data.Date, data.signalMACD, line_color="red", line_width=2.0,
                           legend_label="MACD signal")
            macdChart.vbar(data.Date, w, top=data.histogramMACD)

            macdChart.toolbar.logo = None
            macdChart.border_fill_color = None
            macdChart.title.text_font_size = '16pt'
            macdChart.xaxis.formatter = DatetimeTickFormatter(
                days=["%d/%m/%Y"],
                months=["%d/%m/%Y"],
                years=["%d/%m/%Y"], )
            macdChart.legend.location = "top_left"

            scriptMACD, divMACD = components(macdChart)
    else:
        messages.error(request, "Wrong ticker")
        request.session['ticker'] = None
    return render(request, 'analysis.html',
                  {'today': today, 'day': dayName, 'month': monthName, 'divN': divN, 'scriptN': scriptN, 'divS': divS,
                   'scriptS': scriptS, 'divD': divD, 'scriptD': scriptD, 'scriptMACD': scriptMACD, 'divMACD': divMACD,
                   'ticker': ticker})

def summary(request):
    if request.method == 'POST':
        if 'newgame' in request.POST:
            newToday = TodayDate.objects.all().first()
            newToday.date = "2015-01-02"
            newToday.daysInGame = 0
            newToday.save()
            newMoney= Money.objects.all().first()
            newMoney.cash = 5000
            newMoney.save()
            Stock.objects.all().delete()
            return redirect('home')
    else:
        todayObj = TodayDate.objects.all().first()
        today = todayObj.date
        dayName = today.strftime("%A")
        monthName = today.strftime("%B")
        money = Money.objects.all().first().cash
        portfolio_value = 0
        sharePrice = 0
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            record = []

            # szukanie ktora z kolei jest linia z dzisiejsza data
            date = today.strftime("%Y-%m-%d")
            linenum = 0
            f = open("Stocks/" + ticker_item.ticker + ".us.csv")
            for nr_linii, linia in enumerate(f, start=1):
                if linia.startswith(date):
                    linenum = nr_linii
            linenum = linenum - 1  # wczorajsza data
            values = ""
            sharePrice = 0
            with open("Stocks/" + ticker_item.ticker + ".us.csv") as f:
                for i, line in enumerate(f):
                    if i == linenum:
                        values = line.strip().split(',')
                        sharePrice = float(values[4])
                    elif i > linenum:
                        break
            record.append(ticker_item.ticker)
            record.append(sharePrice)
            record.append(ticker_item.volume)
            record.append(round((sharePrice * ticker_item.volume), 3))
            portfolio_value += sharePrice * ticker_item.volume
            output.append(record)


    portfolio_value = round(portfolio_value, 3)
    total = round(portfolio_value+money,3)
    earnings = round(total-5000,3)
    roi=round((earnings/5000)*100,2)
    return render(request,'summary.html', {'today': today, 'day': dayName, 'month': monthName, 'money': money,
                                              'output': output, 'ticker': ticker, 'portfolio_value': portfolio_value, 'total': total,'earnings':earnings,'roi':roi})
def portfolio(request):
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    money = Money.objects.all().first().cash
    portfolio_value = 0
    sharePrice = 0

    #last day
    if today.strftime("%Y-%m-%d")=='2017-11-10':
        return redirect('summary')

    if request.method == 'POST':
        # formularz zakupu
        if 'buy_button' in request.POST:
            ticker = request.POST.get('buyticker')
            try:
                vol = int(request.POST.get('buyvolume'))
            except:
                vol="Not a number"
            with open("Stocks/tickers.txt", 'r') as plik:
                content = plik.read()
                if ticker in content and isinstance(vol,int):
                    # szukanie ktora z kolei jest linia z dzisiejsza data
                    date = today.strftime("%Y-%m-%d")
                    linenum = 0
                    f = open("Stocks/" + ticker + ".us.csv")
                    for nr_linii, linia in enumerate(f, start=1):
                        if linia.startswith(date):
                            linenum = nr_linii
                    linenum = linenum - 1  # wczorajsza data
                    values=""
                    with open("Stocks/" + ticker + ".us.csv") as f:
                        for i, line in enumerate(f):
                            if i == linenum:
                                values=line.strip().split(',')
                                sharePrice=float(values[4])
                            elif i > linenum:
                                break
                    # szukanie czy w bazie sa juz dane akcje
                    all_stock = Stock.objects.all()
                    new_stock = True
                    for t in all_stock:
                        if t.ticker == ticker:
                            new_stock = False
                            break
                    # sprawdzenie czy mamy wystarczajaco pieniedzy
                    price = float(vol) * sharePrice
                    if (price <= money):
                        if new_stock:
                            newStock = Stock(ticker=ticker, volume=vol)
                            newStock.save()
                        else:
                            new_volume = Stock.objects.get(ticker=ticker).volume + vol
                            Stock.objects.filter(ticker=ticker).update(volume=new_volume)
                        newMoney=Money.objects.all().first()
                        newMoney.cash=round((money - price),3)
                        newMoney.save()
                        messages.success(request, "Added successfully")
                    else:
                        messages.error(request, "Not enough funds")
                    return redirect('portfolio')
                else:
                    messages.error(request, "Wrong values")
                    return redirect('portfolio')
        #formularz sprzedazy
        elif 'sell_button' in request.POST:
            ticker = request.POST.get('sellticker')
            try:
                vol = int(request.POST.get('sellvolume'))
            except:
                vol = "Not a number"
            with open("Stocks/tickers.txt", 'r') as plik:
                content = plik.read()
                if ticker in content and isinstance(vol, int):
                    # szukanie ktora z kolei jest linia z dzisiejsza data
                    date = today.strftime("%Y-%m-%d")
                    linenum = 0
                    f = open("Stocks/" + ticker + ".us.csv")
                    for nr_linii, linia in enumerate(f, start=1):
                        if linia.startswith(date):
                            linenum = nr_linii
                    linenum = linenum - 1  # wczorajsza data
                    values = ""
                    with open("Stocks/" + ticker + ".us.csv") as f:
                        for i, line in enumerate(f):
                            if i == linenum:
                                values = line.strip().split(',')
                                sharePrice = float(values[4])
                            elif i > linenum:
                                break
                    all_stock = Stock.objects.all()
                    new_stock = True
                    for t in all_stock:
                        if t.ticker == ticker:
                            new_stock = False
                            break
                    if new_stock == True:
                        messages.error(request, ("You do not own that shares "))
                        return redirect('portfolio')
                    else:
                        # sprawdzenie czy mamy wystarczajaco sztuk
                        stockvolume = Stock.objects.get(ticker=ticker).volume
                        if vol > stockvolume:
                            messages.error(request, ("You do not own that many shares"))
                            return redirect('portfolio')
                        else:
                            cash = money + vol * sharePrice
                            newMoney = Money.objects.all().first()
                            newMoney.cash = round(cash,3)
                            newMoney.save()
                            new_vol = stockvolume - vol
                            Stock.objects.filter(ticker=ticker).update(volume=new_vol)
                            messages.success(request, ("Sold"))
                            if new_vol == 0:
                                Stock.objects.filter(ticker=ticker).delete()
                            return redirect('portfolio')
                else:
                    messages.error(request, ("Wrong values"))
                    return redirect('portfolio')
        elif 'next_day' in request.POST:
            dates = []
            with open("Stocks/dates.txt", 'r') as p:
                for line in p:
                    dates.append(datetime.strptime(line.strip(), '%Y-%m-%d'))
            # if date.weekday() ==4:
            #     date += timedelta(days=3)  # Przesunięcie do poniedziałku
            # elif date.weekday() < 4:  # Dni od poniedziałku do czwartku
            #     date += timedelta(days=1)
            nextDate = None
            for data in dates:
                if data.date() > today.date():
                    nextDate = data
                    break

            newToday = TodayDate.objects.all().first()
            newToday.date = nextDate.date()
            newToday.daysInGame = newToday.daysInGame+1
            newToday.save()
            return redirect(portfolio)
        elif 'next_week' in request.POST:
            dates = []
            with open("Stocks/dates.txt", 'r') as p:
                for line in p:
                    dates.append(datetime.strptime(line.strip(), '%Y-%m-%d'))
            nextDate = today
            for i in range(5):
                for data in dates:
                    if data.date() > nextDate.date():
                        nextDate = data
                        break
        elif 'next_month' in request.POST:
            dates = []
            with open("Stocks/dates.txt", 'r') as p:
                for line in p:
                    dates.append(datetime.strptime(line.strip(), '%Y-%m-%d'))
            nextDate = today
            for i in range(30):
                for data in dates:
                    if data.date() > nextDate.date():
                        nextDate = data
                        break
            newToday = TodayDate.objects.all().first()
            newToday.date = nextDate.date()
            newToday.daysInGame = newToday.daysInGame+30
            newToday.save()
            return redirect(portfolio)
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            record = []

            # szukanie ktora z kolei jest linia z dzisiejsza data
            date = today.strftime("%Y-%m-%d")
            linenum = 0
            f = open("Stocks/" + ticker_item.ticker + ".us.csv")
            for nr_linii, linia in enumerate(f, start=1):
                if linia.startswith(date):
                    linenum = nr_linii
            linenum = linenum - 1  # wczorajsza data
            values = ""
            sharePrice=0
            with open("Stocks/" + ticker_item.ticker + ".us.csv") as f:
                for i, line in enumerate(f):
                    if i == linenum:
                        values = line.strip().split(',')
                        sharePrice = float(values[4])
                    elif i > linenum:
                        break
            record.append(ticker_item.ticker)
            record.append(sharePrice)
            record.append(ticker_item.volume)
            record.append(round((sharePrice*ticker_item.volume),3))
            portfolio_value+=sharePrice*ticker_item.volume
            output.append(record)
    portfolio_value=round(portfolio_value,3)
    return render(request, 'portfolio.html', {'today': today, 'day': dayName, 'month': monthName, 'money': money,
                                              'output': output, 'ticker': ticker, 'portfolio_value': portfolio_value})


def education(request):
    return render(request, 'education.html')


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
