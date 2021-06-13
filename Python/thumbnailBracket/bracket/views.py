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

dateFormat = '%Y-%m-%dT%H:%M:%S'

def index(request):
    kwargs = {}
    return render(request, 'index.html',kwargs)

def leaderboard(request):
    kwargs = {}
    kwargs['leaders'] = getLeaders()

    return render(request, 'leaderboard.html',kwargs)

def test(request):
    """
    throw whatever functionality here for debugging
    """
    results = runSql( sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit 100;')
    getLeaders()
    return HttpResponse(results)

def vote(request, ytid1 = None, ytid2 = None):
    #TODO: return more metadata
    if not request.session.session_key:
        request.session['created']=datetime.datetime.now().strftime(dateFormat)
    choices = {}
    choices['left'] =  getRandYtidMeta()
    choices['vs'] = 'vs'
    choices['right'] = getRandYtidMeta()
    context = {'choices':choices}    
    infoTableMap = {
        'upload_date':{
            'displayName':'Uploaded',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y%m%d').strftime('%Y %b %d'),
            #'rank':1,
        },
        'duration':{
            'displayName':'Length',
            'transformFunction': lambda x: datetime.timedelta(seconds = x),
            #'rank':2,
        },
        'view_count':{
            'displayName':'Views',
            #'rank':3,
        },
        'like_count':{
            'displayName':'Likes',
            #'rank':4,
        },
        'dislike_count':{
            'displayName':'Dislikes',
            #'rank':5,
        },
        'webpage_url':{
            'displayName':'link',
            'transformFunction': lambda x: f'<a href="{x}">!-----!</a>',
            #'rank':6,
        },
    }
    #set a display key in choice dict that will be what shows on the ytInfoTable div 
    for choice in context['choices'].values():
        infoTable = {}
        if choice == 'vs':
            continue

        for k,v in choice.items():
            if not infoTableMap.get(k):
                continue
            displayName = infoTableMap[k]['displayName']          

            transform = infoTableMap[k].get('transformFunction')
            if transform:
                displayValue = transform(v)
                if k == 'webpage_url':
                    #after transforming the display value, make the anchor inner text be the video title
                    displayValue =  displayValue.replace('!-----!',choice['title'])
            else:
                displayValue = v

            infoTable[displayName] = displayValue
        choice['ytMetadata'] = infoTable
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
    Can take bind variables in the standard sqlite3 module styles
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

        cur.execute(sql)
        results = cur.fetchall()
        return results

def getLeaders() -> list:
    """
    idk what, not working
    """
    sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit 100;'
    results = runSql(sql)
    leaders = []
    while results:
        v, count = results.pop()
        print(v)
        v = getVideoMetadata(v)
        pprint(v)
        leaders.append(v)
    return(leaders)



#http://127.0.0.1:8000/vote/LipcFI8tq_I-7H3VhvU_2Aw

if __name__ == '__main__':
    print(getVideoMetadata('c1mhLFuiGeg'))