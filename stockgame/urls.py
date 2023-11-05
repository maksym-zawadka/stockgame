"""
URL configuration for stockgame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game import views
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('analysis/', views.analysis, name="analysis"),
    path('portfolio/', views.portfolio, name="portfolio"),
    path('education/', views.education, name="education"),
    path('dopasowania/', views.dopasowania, name='dopasowania'),
    path('fullname/', views.fullname, name='fullname'),
    path('summary/', views.summary, name='summary'),
    path('education/what-is-sma.html', lambda request: render(request, 'education/what-is-sma.html'), name='sma'),
    path('education/what-is-ema.html', lambda request: render(request, 'education/what-is-ema.html'), name='ema'),
    path('education/understanding-investing.html',
         lambda request: render(request, 'education/understanding-investing.html'), name='investing'),
    path('education/what-is-stock.html',
         lambda request: render(request, 'education/what-is-stock.html'), name='stock'),
    path('education/what-is-ticker.html',
         lambda request: render(request, 'education/what-is-ticker.html'), name='ticker'),
    path('education/what-are-bb.html',
         lambda request: render(request, 'education/what-are-bb.html'), name='bb'),
    path('education/what-is-macd.html',
         lambda request: render(request, 'education/what-is-macd.html'), name='macd'),
    path('education/understanding-indicators.html',
         lambda request: render(request, 'education/understanding-indicators.html'), name='indicators'),
]
