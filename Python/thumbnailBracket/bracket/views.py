import datetime
from pathlib import Path
from pprint import pformat, pprint
import datetime

from django.core.cache import caches
from django.views.decorators.cache import cache_control, cache_page
from django.http import HttpResponse
from django.shortcuts import render
from django.urls.resolvers import LocalePrefixPattern #urlencode, 
from django.db import connection
from urllib.parse import quote

try:
    from bracket.common import (logger, metadataByYtid, 
                                getVoteOption, getClientIP, 
                                runSql, metadataDisplayMap, 
                                addMatchHistoryMetadata
                                ,datetimeFormat)
    from bracket.models import *
except Exception as e:
    print("couldn't import custom django modules common and models\n", e)
    raise

with open('sql/leaderboardQuery.sql','r') as f:
    leaderboardQuery = f.read()

@cache_page(60 * 15)
def index(request):
    kwargs = {}
    return render(request, 'index.html',kwargs)

def test(request):
    """
    throw whatever functionality here for debugging
    """
    results = runSql( sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit 100;')
    #getLeaders()
    return HttpResponse(results)

@cache_page(60*1)
def stats(request, ytid):
    metadata = metadataByYtid[ytid]
    metadata = addMatchHistoryMetadata(metadata, fullHist = True)
    displayMetadata = metadataDisplayMap(metadata)
    #print(metadata)
    opponentMetadataList = []
    for match in metadata['matchHistory']:
        opponentMetadata = metadataByYtid[match.opponentYtid]
        opponentMetadata['outcome'] = match.outcome
        opponentMetadata['voteDatetime'] = match.voteDatetime
        opponentMetadata['displayMetadata'] = metadataDisplayMap(opponentMetadata)
        opponentMetadataList.append(opponentMetadata)
    del metadata['matchHistory']
    context = {'ytVid':metadataByYtid[ytid],
               'ytMetadata': displayMetadata,
                'opponentMetadataList':opponentMetadataList,
    }
    print(context)
    #import pdb; pdb.set_trace()
    #template = if match then show thumbnail and win/loss
    #each thumbnail links to stats for that one
    return render(request, 'stats.html', context)

@cache_page(60 * 1)
def leaderboard(request, resultLimit:int = 24) -> list:
    global leaderboardQuery
    """
    TODO: docstring
    """
    params = {'resultLimit':resultLimit }

    #sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit :resultLimit;'
    results = runSql(leaderboardQuery,params)

    leaders = []
    for ytId, wins in results:        
        metadata = metadataByYtid[ytId]
        metadata['wins'] = wins
        leaders.append(metadata)
    leaders = [(rank + 1, metadata, metadataDisplayMap(addMatchHistoryMetadata(metadata))) for rank,metadata in enumerate(leaders)]
    kwargs = {}
    kwargs['leaders'] = leaders
    return render(request, 'leaderboard.html',kwargs)

@cache_control(private=True)
def vote(request, ytid1 = None, ytid2 = None):
    #TODO: Voting needs to update the wins/losses in metadataByYtid
    #TODO: need to make metadataByYtid a database thing instead of all in memory
    if not request.session.session_key:
        request.session['created']=datetime.datetime.now().strftime(datetimeFormat)
    """
        >>> caches['default'].set('key', 'value', 60)  # 60 seconds
        >>> caches['default'].get('key')
        'value
        >>> caches['idempotent_tokens'].set(uuid, datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))
        >>> if caches['idempotent_tokens'].get(uuid):
        >>>     duplicate request
        >>> else:
        >>>     valid request
    """
    choices = {}
    #TODO: choices is a dict and probably should be a list, template would need to change
    choices['left'] =  addMatchHistoryMetadata(getVoteOption())
    choices['vs'] = 'vs'
    choices['right'] = addMatchHistoryMetadata(getVoteOption())
    context = {'choices':choices}    

    while choices['right'] == choices['left']:
        choices['right'] = addMatchHistoryMetadata(getVoteOption())
        4443
    #set a display key in choice dict that will be what shows on the ytVidMetaTable div 
    for choice in context['choices'].values():
        if choice == 'vs':
            continue        
        choice['displayMetadata'] = metadataDisplayMap(choice)
    #choices = intersperse(choices, 'vs')
    if request.method == 'GET':
        response = render(request, 'vote.html', context)
    if request.method == 'POST':
        print(request.POST)
        vote = Vote (**{
            'loseYtid': request.POST['lose'],
            'winYtid': request.POST['win'],
            'ytChannel': 'KingCobraJFS',
            'postingIP': getClientIP(request), 
            'session': request.session.session_key,
        })
        #import pdb; pdb.set_trace()
        vote.save()
        print(vote)
        response = render(request, 'voteContainer.html', context)
    #TODO: add a vote history thing to vote screen that links to a full history screen and shows recent votes
    #context['lastVotes'] = runSql("""select
    #                                         winYtid
    #                                        ,loseYtid  
    #                                   from vote 
    #                                   where session = :sessionId
    #                                   limit 5;"""
    #                            , request.session.session_key
    #                            , 'Winner Loser'
    #                            )
    return response  

if __name__ == '__main__':
    pass