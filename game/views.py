from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import TodayDate
import plotly.graph_objects as go
import pandas as pd
import plotly.offline as opy

def home(request):
    return render(request, 'home.html')


def analysis(request):
    #today date
    todayObj=TodayDate.objects.all().first()
    today=todayObj.date
    dayName=today.strftime("%A")
    monthName=today.strftime("%B")

    #chart
    df=pd.read_csv("Stocks/ndx.txt", sep=',')

    fig= go.Figure(data=[go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])])
    fig_div = opy.plot(fig, output_type='div', auto_open=False)

    return render(request, 'analysis.html', {'today': today,'day':dayName, 'month':monthName, 'fig':fig_div} )