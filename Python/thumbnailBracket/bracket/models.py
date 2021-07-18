import uuid
import datetime

from django.db import models
from django.utils import timezone

dateFormat = '%Y-%b-%d'
datetimeFormat = '%Y-%b-%d %H:%M:%S'

#outcomes       = [('W','Win'),('D','Draw'),('L','Loss')]
#allowedOutcomes    = [x[0] for x in outcomes] #used if I ever need to reference outcomes elsewhere in the code
class outcomes(models.TextChoices):
    WIN     = 'W'
    DRAW    = 'D'
    LOSS    = 'L'

#TODO: Deprecate Vote entirely and replace with betterVote
class Vote(models.Model):
    print('deprecation warning on vote model, switch to better vote logic')
    loseYtid       = models.CharField(max_length=200)
    winYtid        = models.CharField(max_length=200)
    ytChannel      =  models.CharField(max_length=50)
    voteDatetime   = models.DateTimeField(default = timezone.now)
    postingIP      = models.CharField(max_length=200) 
    session        = models.CharField(max_length=200)
    
    class Meta:
        indexes = [
            models.Index(fields=['winYtid', 'ytChannel'], name='win_idx'),
            models.Index(fields=['loseYtid', 'ytChannel'], name='lose_idx'),
        ]

class YtVid(models.Model):
    ytChannel      = models.CharField(max_length=50) #uploader_url
    ytid           = models.CharField(max_length = 200, unique=True) #id
    title          = models.CharField(max_length = 200) #title
    thumbnail      = models.CharField(max_length = 200) #thumbnail
    like_count     = models.IntegerField() #same
    dislike_count  = models.IntegerField() #same
    view_count     = models.IntegerField() #same
    duration       = models.IntegerField()  #same
    webpage_url    = models.CharField(max_length = 200)  #same
    upload_date    = models.DateField()  #same
    score          = models.IntegerField(default=0, help_text="elo score, or placeholder value for rank")
    votes          = models.IntegerField(default=0) 
    wins           = models.IntegerField(default=0)
    draws          = models.IntegerField(default=0)
    losses         = models.IntegerField(default=0)
    winRatio       = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def updateStats(self, outcome):
        if outcome not in outcomes:
            msg = f"{outcome} not a valid outcome type. valid types are {[x for x in outcomes]}"
            raise TypeError(msg)
        self.votes += 1
        if outcome   == 'W':
            self.wins += 1
        elif outcome == 'D':
            self.draws += 1
        elif outcome == 'L':
            self.losses += 1 
        else:
            raise NotImplementedError
        self.winRatio = self.wins / self.votes

    def calculateDisplayAttrs(self):
        """adds display values to object
        works with the ytVidMetaTable.html include"""
        def vidLength(x):
            totalSecs = int(x)
            h = totalSecs//3600
            if h>1:
                hText=f'{h} hours'
            elif h==1:
                hText=f'{h} hour'
            else:
                hText=''
            m = (totalSecs%3600) // 60
            if m>1:
                mText=f'{m} minutes'
            elif m==1:
                mText=f'{m} minute'
            else:
                mText=''
            #sec =(totalSecs%3600)%60 #just for reference
            return f'{hText} {mText}'
        infoTableMap = {
            'upload_date':{
                'displayName':'Uploaded',
                'transformFunction': lambda x: x.strftime(dateFormat),#lambda x: datetime.datetime.strptime(x,'%Y%m%d').strftime(dateFormat),
            },
            'duration':{
                'displayName':'Length',
                'transformFunction': vidLength #lambda x: datetime.timedelta(seconds=x)
            },
            'view_count':{
                'displayName':'Views',
                'transformFunction': lambda x: "{:,}".format(int(x))
            },
            'webpage_url':{
                'displayName':'link',
                'transformFunction': lambda x: f'<a href="{x}" target="_blank">!-----!</a>',
            },
            'voteDatetime':{
                'displayName':'Vote Time',
                'transformFunction': lambda x: x.strftime(datetimeFormat),#datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime(datetimeFormat),
            },
            #'winRatio':{ #TODO: this is a test line in the infoTable
            #    'displayName':'Stats/Win/Loss/%',
            #    'transformFunction': lambda x: str(int(x *100)) + '%'#lambda x: f'<a href="/stats/{metadata.id}" target="_blank">Stats - </a>',
            #},
        }
        displayDict = {}
        print(vars(self))
        for k,v in vars(self).items():
            if k == 'title':
                title = v
                continue
            if not infoTableMap.get(k):
                continue
            displayName = infoTableMap[k]['displayName']          

            transform   = infoTableMap[k].get('transformFunction')
            if transform:
                print(transform, k, v)
                displayValue = transform(v)
            else:
                displayValue = v
            displayDict[displayName] = displayValue
        
        if self.dislike_count:
            likeRatio = float(self.like_count)/(float(self.like_count) + float(self.dislike_count))
        else:
            likeRatio = self.like_count
        
        likeRatio *= 100
        likeRatio  = str(int(likeRatio)) + '%'

        displayDict['Likes/Dislikes/%'] = (f"<span class='text-success'>{self.like_count}</span>"
                                        f"/<span class='text-danger'>{self.dislike_count}</span>"
                                        f"/{likeRatio}"
        )
        #after transforming the display value, make the anchor inner text be the video title
        displayDict['link'] = displayDict['link'].replace('!-----!',title)

        displayDict['Wins/Losses/%'] = (#f"<a href='/stats/{self.id}' target='_blank'>Stats</a> - "
                                            f"<span class='text-success'>{self.wins}</span>"
                                            f"/<span class='text-danger'>{self.losses}</span>"
                                            f"/{str(int(self.winRatio *100))}%"
        )
        #displayDict['Stats/Wins/Losses/%'] = 'test'
        return displayDict

    def __str__(self):
        return f"{self.ytid} - {self.title} - {self.upload_date} - {self.score}"
    
    class Meta:
        indexes = [
            models.Index(fields=['ytChannel', 'ytid', 'votes', 'wins'], name='ytVid_idx'),
            #models.Index(fields=['ytChannel', 'session', 'voteDatetime'], name='ytid_idx'),
        ]

        constraints =  [
            models.UniqueConstraint(fields=['ytChannel', 'ytid'], name='unique_booking')
        ]

class statManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related().order_by('-voteDatetime')

#class voteEvent(models.Model):
#    voteID         = models.CharField(max_length=50, help_text="used to tie a group of votes together as being part of the same decision")
    

class betterVote(models.Model):
    voteID         = models.CharField(max_length=50, help_text="used to tie a group of votes together as being part of the same decision")
    ytVid          = models.ForeignKey(YtVid, on_delete=models.CASCADE)
    outcome        = models.CharField(max_length=10, choices=outcomes.choices)
    postingIP      = models.CharField(max_length=200) 
    session        = models.CharField(max_length=200)
    voteDatetime   = models.DateTimeField(default = timezone.now)
    
    objects        = models.Manager()
    stats          = statManager()
    #usage - betterVote.stats.exclude('id that i'm currently on in /stats/')
    def __str__(self):
        return f"{self.voteID} - {self.ytVid.id} - {self.outcome}"

    #TODO: experiment with overwriting the save function on betterVote to maintain the stats on YtVid
    #def save(self, *args, **kwargs):
    #    if getattr(self, '_image_changed', True):
    #        small=rescale_image(self.image,width=100,height=100)
    #        self.image_small=SimpleUploadedFile(name,small_pic)
    #    super(Model, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['ytVid', 'outcome'], name='vote_outcome_idx'),
            models.Index(fields=['session', 'voteDatetime'], name='ytid_idx'),
        ]
        