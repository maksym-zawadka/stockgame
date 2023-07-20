from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import TodayDate
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as opy
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Range1d,WheelZoomTool
from bokeh.embed import components
from bokeh.io import output_notebook,show

def home(request):
    return render(request, 'home.html')

def analysis(request):
    # today date
    todayObj = TodayDate.objects.all().first()
    today = todayObj.date
    dayName = today.strftime("%A")
    monthName = today.strftime("%B")
    daysInGame = 0
    # chart
    # 1258 - ostatni dzien z przed rozpoczeciem
    df = pd.read_csv("Stocks/ndx.txt", sep=',', header=0, encoding='utf-16', nrows=100 + daysInGame)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    df['Date'] = pd.to_datetime(df['Date'])
    source = ColumnDataSource(df)

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12 * 60 * 60 * 1000  # half day in ms
    # Tworzenie wykresu świecowego
    p = figure(x_axis_type='datetime', title='Candlestick Chart', width=1200, height=600, sizing_mode="fixed", tools="")
    p.segment(x0='Date', y0='High', x1='Date', y1='Low', source=source, color="black")
    p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="green", line_color="black")
    p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="red", line_color="black")

    script, div = components(p)

    # fig = go.Figure(
    #     data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    # config = {
    #     'displayModeBar': False
    # }
    # fig.update_layout(hovermode=False,
    #                   paper_bgcolor='rgba(0,0,0,0)',
    #                   xaxis=dict(fixedrange=True),
    #                   yaxis=dict(fixedrange=True),
    #                   title="Nasdaq 100 (^NDX)")
    # fig.update_xaxes(range=[today - relativedelta(years=1), today], rangeslider=dict(visible=True))
    # fig.update_yaxes(autorange=True)
    # fig_div = opy.plot(fig, output_type='div', auto_open=False, show_link=False, config=config)

    return render(request, 'analysis.html', {'today': today, 'day': dayName, 'month': monthName, 'div': div, 'script':script})
