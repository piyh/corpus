import datetime
from django.db import models
from django.utils import timezone

#dateFormat = '%Y-%m-%dT%H:%M:%S'

class Vote(models.Model):
    loseYtid      = models.CharField(max_length=200)
    winYtid     = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default = timezone.now)
    postingIP      = models.CharField(max_length=200) # HttpRequest.get_host()
    session        = models.CharField(max_length=200)
    #TODO: cookie id here

class Leaderboard(models.Model):
    ytid       = models.CharField(max_length=200)
    rank       = models.IntegerField()
    wins       = models.IntegerField()
    losses     = models.IntegerField()
