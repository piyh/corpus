from django.db import models

class Thumbnail(models.Model):
    ytid  = models.CharField(max_length=200)
	idTwo  = models.CharField(max_length=200)
	winner = models.CharField(max_length=200)

class HeadToHead(models.Model):
    ytidOne  = models.ForeignKey(on_delete=models.CASCADE)
	ytidTwo  = models.ForeignKey(on_delete=models.CASCADE)
	winner = models.CharField(max_length=200)
    selection_date = models.DateTimeField('date selection was made')
    postingIP = models.CharField(max_length=200)
