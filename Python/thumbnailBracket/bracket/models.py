import datetime
from django.db import models
from django.utils import timezone

#dateFormat = '%Y-%m-%dT%H:%M:%S'

class Vote(models.Model):
    loseYtid       = models.CharField(max_length=200)
    winYtid        = models.CharField(max_length=200)
    timestamp      = models.DateTimeField(default = timezone.now)
    postingIP      = models.CharField(max_length=200) # HttpRequest.get_host()
    session        = models.CharField(max_length=200)
    #TODO: cookie id here

class Leaderboard(models.Model):
    ytid       = models.CharField(max_length=200)
    rank       = models.IntegerField()
    wins       = models.IntegerField()
    losses     = models.IntegerField()

class ytVid(models.Model):
    ytid= models.CharField(max_length = 200, primary_key=True)
    title= models.CharField(max_length = 200)
    thumbnail= models.CharField(max_length = 200)
    like_count= models.IntegerField()
    dislike_count= models.IntegerField()
    view_count= models.IntegerField()
    duration= models.IntegerField()
    webpage_url= models.CharField(max_length = 200)
    upload_date= models.CharField(max_length = 200)

class nonce(models.Model):
    nonce = models.CharField(max_length = 200, primary_key=True)
    datetime = models.DateTimeField(default = timezone.now)