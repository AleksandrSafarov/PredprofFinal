from django.db import models

class Flight(models.Model):
    flightid = models.IntegerField()
    pointid = models.IntegerField()
    sh = models.IntegerField()
    distance = models.IntegerField()