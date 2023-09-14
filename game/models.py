from django.db import models


# Create your models here.

class TodayDate(models.Model):
    date = models.DateTimeField(null=False, default="2010-01-04")
    daysInGame = models.IntegerField(null=False, default=0)


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    volume = models.IntegerField(null=True, default=0)


class Money(models.Model):
    cash = models.FloatField(null=True)

class Portfolio(models.Model):
    date = models.DateTimeField(null=False, default="2010-01-04")
    portfolioValue = models.FloatField(null=True)