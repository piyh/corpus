import datetime
from pathlib import Path
from pprint import pformat, pprint
import datetime
from urllib.parse import quote
from uuid import uuid4

from django.core.cache import caches
from django.views.decorators.cache import cache_control, cache_page
from django.http import HttpResponse
from django.shortcuts import render
from django.urls.resolvers import LocalePrefixPattern #urlencode, 
from django.db import connection, transaction

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
def stats(request, ytVidID):
    #ytid = YtVid.objects.get(id=ytid).ytid
    ytVid = YtVid.objects.get(id=ytVidID)
    displayMetadata = ytVid.calculateDisplayAttrs()
    #metadata = metadataByYtid[ytid]
    voteIDs = betterVote.objects.select_related().filter(ytVid=ytVid).values('voteID') #find all vote IDs the master YTID has been part of
    votes = betterVote.objects.select_related().filter(voteID__in=voteIDs).exclude(ytVid=ytVid) #take those vote IDs and look for the opponent
    #metadata = addMatchHistoryMetadata(metadata, fullHist = True)
    #print(metadata)
    opponentList = []
    for vote in votes:
        opponentVid = vote.ytVid
        if vote.outcome == 'W':
            #flip the vote since we're seeing if the opponent won or lost instead if the ytid won or lost 
            opponentVid.outcome = 'L'
        elif vote.outcome == 'L':
            opponentVid.outcome = 'W'
        opponentVid.displayMetadata = opponentVid.calculateDisplayAttrs()
        opponentList.append(opponentVid)
    context = {'ytVid':ytVid,
               'ytMetadata': displayMetadata,
                'opponentList':opponentList,
    }
    print(context)
    #import pdb; pdb.set_trace()
    #template = if match then show thumbnail and win/loss
    #each thumbnail links to stats for that one
    return render(request, 'stats.html', context)

@cache_page(60 * 1)
def leaderboard(request, resultLimit:int = 24) -> list:
    """
    get the best thumbnails and 
    """
    params = {'resultLimit':resultLimit }
    #global leaderboardQuery
    #sql = 'select winYtid, count(*) from bracket_vote group by winYtid order by count(*) desc limit :resultLimit;'
    #results = runSql(leaderboardQuery,params)

    #leaders = [(rank + 1, ytVidID) for rank, (ytVidID, _) in enumerate(results)]

    #for ytId, _ in results:        
    #ytVids = YtVid.objects.filter(pk__in = [ytVidID for rank, ytVidID in leaders])
    #ytVids = {x.id:x for x in ytVids}
    #objectMappedLeaders = []
    #while leaders:
    #    rank, ytVidID = leaders.pop()
    #    ytVid = ytVids[ytVidID]
    #    objectMappedLeaders.insert(0,(rank, ytVid))
    #leaders = objectMappedLeaders
    #for rank, leader in leaders:
    #    leader.score = rank
    #    leader.save()
    #print(betterVote.objects.filter(ytVid__in=[x.id for rank,x in leaders]))
    #print(betterVote.objects.exclude(ytVid__score=0).order_by('-ytVid__score')) #objects.select_related().get(id=2)
    leaders = YtVid.objects.order_by('-wins', 'votes')[:resultLimit] #TODO: '-score'
    #leaders = [(rank + 1, metadata, metadataDisplayMap(metadata)) for metadata in leaders]
    #[x.calculateDisplayAttrs() for x in leaders]
    leaders = [(rank + 1, leader, leader.calculateDisplayAttrs()) for rank,leader in enumerate(leaders)]
    kwargs = {}
    kwargs['leaders'] = leaders
    return render(request, 'leaderboard.html',kwargs)

@cache_control(private=True)
@transaction.atomic
def vote(request, ytid1 = None, ytid2 = None):
    #TODO: Voting needs to update the wins/losses in metadataByYtid
    #TODO: need to make metadataByYtid a database thing instead of all in memory
    if not request.session.session_key:
        request.session['created']=datetime.datetime.now().strftime(datetimeFormat)
    choices = {}
    #TODO: choices is a dict and probably should be a list, template would need to change
    choices['left'] =  addMatchHistoryMetadata(getVoteOption())#.calculateDisplayAttrs()
    choices['vs'] = 'vs'
    choices['right'] = addMatchHistoryMetadata(getVoteOption())
    context = {'choices':choices}    

    while choices['right'] == choices['left']:
        choices['right'] = addMatchHistoryMetadata(getVoteOption())

    #set a display key in choice dict that will be what shows on the ytVidMetaTable div 
    for choice in context['choices'].values():
        if choice == 'vs':
            continue        
        choice['displayMetadata'] = metadataDisplayMap(choice)
    #choices = intersperse(choices, 'vs')
    """
        #HOW TO USE DJANGO CACHES IN A NUTSHELL
        >>> caches['default'].set('key', 'value', 60)  # 60 seconds
        >>> caches['default'].get('key')
        'value
        >>> caches['idempotent_tokens'].set(uuid, datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))
        >>> if caches['idempotent_tokens'].get(uuid):
        >>>     duplicate request
        >>> else:
        >>>     valid request
    """
    idempotentUuid = uuid4()
    context['idempotent_token'] = idempotentUuid
    caches['idempotent_tokens'].set(uuid, datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))
    if request.method == 'GET':
        response = render(request, 'vote.html', context)
    if request.method == 'POST':
        if caches['idempotent_tokens'].get(request.POST['idempotent_token']):
            logger.debug(f"duplicate idempotent token {request.POST['idempotent_token']}, vote ignored")
            response = render(request, 'voteContainer.html', context)
        print(request.POST)
        #vote = Vote (**{
        #    'loseYtid': request.POST['lose'],
        #    'winYtid': request.POST['win'],
        #    'ytChannel': 'KingCobraJFS',
        #    'postingIP': getClientIP(request), 
        #    'session': request.session.session_key,
        #})
        #vote.save()
        #print(vote)
        loseVid = YtVid.objects.get(ytid=request.POST['lose']) #TODO: switch from ytid to surrogate keys across app
        winVid  = YtVid.objects.get(ytid=request.POST['win'])
        loseVid.updateStats('L')
        winVid.updateStats('W')
        winVid.save()
        loseVid.save()

        voteID = uuid4()
        normalizedVoteWin = betterVote(**{
            'voteID': voteID,
            'ytVid': winVid,
            'outcome': 'W',
            'postingIP': getClientIP(request),  
            'session': request.session.session_key,
        })
        normalizedVoteLoss = betterVote(**{
            'voteID': voteID,
            'ytVid': loseVid,
            'outcome': 'L',
            'postingIP': getClientIP(request),
            'session': request.session.session_key,
        })
        print(f"created normalized votes {request.POST['lose']} and {request.POST['win']}")
        normalizedVoteLoss.save()
        normalizedVoteWin.save()
        print('returning render')
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