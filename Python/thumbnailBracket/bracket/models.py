from django.db import models

class Thumbnail(models.Model):
    ytid    = models.CharField(max_length=200)
    path    = models.CharField(max_length=800)
    name    = models.CharField(max_length=800)
    created = models.DateTimeField('created date for given ytid')

class Vote(models.Model):
    thumbnailOne   = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name = 'first')
    thumbnailTwo   = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name = 'second')
    winner         = models.CharField(max_length=200)
    selection_date = models.DateTimeField('date selection was made')
    postingIP      = models.CharField(max_length=200) # HttpRequest.get_host()
    session        = models.CharField(max_length=200)
    #TODO: cookie id here

class Leaderboard(models.Model):
    thumbnail  = models.ForeignKey(Thumbnail, on_delete=models.CASCADE)
    rank       = models.IntegerField()
    wins       = models.IntegerField()
    losses     = models.IntegerField()