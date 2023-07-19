from django.db import models


# Create your models here.

class TodayDate(models.Model):
    date = models.DateTimeField(null=False, default="2010-01-04")
