from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import TodayDate
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as opy
from dateutil.relativedelta import relativedelta


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
    df = pd.read_csv("Stocks/ndx.txt", sep=',', header=0, encoding='utf-16',nrows=1258+daysInGame)

    fig = go.Figure(
        data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    config = {
        'displayModeBar': False
    }
    fig.update_layout(hovermode=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(fixedrange=True),
                      yaxis=dict(fixedrange=True),
                      title="Nasdaq 100 (^NDX)")
    fig.update_xaxes(range=[today - relativedelta(years=1), today], rangeslider=dict(visible=True))
    fig.update_yaxes(autorange=True)
    fig_div = opy.plot(fig, output_type='div', auto_open=False, show_link=False, config=config)

    return render(request, 'analysis.html', {'today': today, 'day': dayName, 'month': monthName, 'fig': fig_div})
