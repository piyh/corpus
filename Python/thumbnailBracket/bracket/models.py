from django.db import models
from django.utils import timezone

class Vote(models.Model):
    loseYtid       = models.CharField(max_length=200)
    winYtid        = models.CharField(max_length=200)
    ytChannel      =  models.CharField(max_length=50)
    voteDatetime   = models.DateTimeField(default = timezone.now)
    postingIP      = models.CharField(max_length=200) # HttpRequest.get_host()
    session        = models.CharField(max_length=200)
    
    class Meta:
        indexes = [
            models.Index(fields=['winYtid', 'ytChannel'], name='win_idx'),
            models.Index(fields=['loseYtid', 'ytChannel'], name='lose_idx'),
        ]

class betterVote(models.Model):
    nonce          = models.CharField(max_length=50)
    ytid           = models.CharField(max_length=50)
    ytChannel      = models.CharField(max_length=50)
    voteDatetime   = models.DateTimeField(default = timezone.now)
    postingIP      = models.CharField(max_length=200) # HttpRequest.get_host()
    session        = models.CharField(max_length=200)
    
    class Meta:
        indexes = [
            models.Index(fields=['nonce', 'ytChannel'], name='nonce_idx'),
            models.Index(fields=['ytid', 'ytChannel'], name='ytid_idx'),
        ]

#class Leaderboard(models.Model):
#    ytid       = models.CharField(max_length=200)
#    rank       = models.IntegerField()
#    wins       = models.IntegerField()
#    losses     = models.IntegerField()

class YtVid(models.Model):
    ytid= models.CharField(max_length = 200, primary_key=True)
    title= models.CharField(max_length = 200)
    thumbnail= models.CharField(max_length = 200)
    like_count= models.IntegerField()
    dislike_count= models.IntegerField()
    view_count= models.IntegerField()
    duration= models.IntegerField()
    webpage_url= models.CharField(max_length = 200)
    upload_date= models.DateField()
    votes = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

class nonce(models.Model):
    nonce = models.CharField(max_length = 200, primary_key=True)
    nonceDatetime = models.DateTimeField(default = timezone.now)\

    