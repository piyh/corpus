import datetime
from pathlib import Path
from pprint import pformat, pprint
import sqlite3
import random
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.urls.resolvers import LocalePrefixPattern #urlencode, 
from django.db import connection
from urllib.parse import quote

try:
    from bracket.common import config, channelDir, logger, metadata, getRandYtidMeta
    from bracket.models import *
except Exception as e:
    print("couldn't import custom django modules common and models\n", e)
    raise

dateFormat = '%Y-%m-%dT%H:%M:%S'

def index(request):
    kwargs = {}
    return render(request, 'index.html',kwargs)

def test(request):
    """
    throw whatever functionality here for debugging
    """
    results = runSql( sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit 100;')
    getLeaders()
    return HttpResponse('hi')

def leaderboard(request, resultLimit:int = 24) -> list:
    """
    TODO: docstring
    """
    params = {'resultLimit':resultLimit }
    sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit :resultLimit;'
    results = runSql(sql,params)

    leaders = []
    for ytId, wins in results:        
        metadatum = metadata[ytId]
        metadatum['wins'] = wins
        leaders.append(metadatum)
    leaders = [(rank + 1, metadatum, metadatumDisplayMap(metadatum)) for rank,metadatum in enumerate(leaders)]
    kwargs = {}
    kwargs['leaders'] = leaders
    return render(request, 'leaderboard.html',kwargs)

def metadatumDisplayMap(metadatum:dict) -> dict:
    """takes an info json and returns a new dict that has display values for the ytVidMetaTable.html include"""
    infoTableMap = {
        'upload_date':{
            'displayName':'Uploaded',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y%m%d').strftime('%Y %b %d'),
        },
        'duration':{
            'displayName':'Length',
            'transformFunction': lambda x: datetime.timedelta(seconds = x),
        },
        'view_count':{
            'displayName':'Views',
        },
        'like_count':{
            'displayName':'Likes',
        },
        'dislike_count':{
            'displayName':'Dislikes',
        },
        'webpage_url':{
            'displayName':'link',
            'transformFunction': lambda x: f'<a href="{x}" target="_blank">!-----!</a>',
        },
    }
    displayDict = {}
    for k,v in metadatum.items():
        if k == 'title':
            title = v
            continue
        if not infoTableMap.get(k):
            continue
        displayName = infoTableMap[k]['displayName']          

        transform = infoTableMap[k].get('transformFunction')
        if transform:
            displayValue = transform(v)
        else:
            displayValue = v
        displayDict[displayName] = displayValue
    
    #after transforming the display value, make the anchor inner text be the video title
    displayDict['link'] = displayDict['link'].replace('!-----!',title)
    return displayDict

def vote(request, ytid1 = None, ytid2 = None):
    if not request.session.session_key:
        request.session['created']=datetime.datetime.now().strftime(dateFormat)
    choices = {}
    choices['left'] =  getRandYtidMeta()
    choices['vs'] = 'vs'
    choices['right'] = getRandYtidMeta()
    context = {'choices':choices}    

    #set a display key in choice dict that will be what shows on the ytVidMetaTable div 
    for choice in context['choices'].values():
        if choice == 'vs':
            continue        
        choice['ytMetadata'] = metadatumDisplayMap(choice)
    #choices = intersperse(choices, 'vs')
    if request.method == 'GET':
        response = render(request, 'vote.html', context)
    if request.method == 'POST':
        print(request.POST)
        vote = Vote (**{
            'loseYtid': request.POST['lose'],
            'winYtid': request.POST['win'],
            'postingIP': getClientIP(request), 
            'session': request.session.session_key,
        })
        #import pdb; pdb.set_trace()
        vote.save()
        print(vote)
        response = render(request, 'voteContainer.html', context)

    return response  

def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def runSql(sql: str,bindVariables: list = None) -> list:
    """
    runs sql that should be read only against the django sqlite db.  
    Can take bind variables in the standard sqlite3 module styles.
    """
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor() 
            # bind style
            #cur.execute("select * from lang where first_appeared=:year", {"year": 1972})

            # The qmark style used with executemany():
            #lang_list = [
            #    ("Fortran", 1957),
            #    ("Python", 1991),
            #    ("Go", 2009),
            #]
            #cur.executemany("insert into lang values (?, ?)", lang_list)
        args = [sql]
        if bindVariables:
            args.append(bindVariables)
        cur.execute(*args)
        results = cur.fetchall()
        return results
        
if __name__ == '__main__':
    print(getVideoMetadata('c1mhLFuiGeg'))