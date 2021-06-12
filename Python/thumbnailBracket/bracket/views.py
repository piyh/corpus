import random
from pathlib import Path
from configparser import ConfigParser
import json
from pprint import pformat, pprint
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote
from .common import config, channelDir, thumbnailExtensions, logger
from .models import *
from django.urls.resolvers import LocalePrefixPattern #urlencode, 
import datetime
dateFormat = '%Y-%m-%dT%H:%M:%S'

def findFile(ytid: str, extensions: set[str]) -> Path:
    for file in channelDir.iterdir():
        if (    file.is_file()
                and ytid in file.name
                and set(file.suffixes).intersection(extensions)):
            return file
    else:
        logger.exception(f"couldn't {ytid} with extensions {extensions}")
        raise FileNotFoundError('Could not find ytid')

def index(request):
    kwargs = {}
    return render(request, 'index.html',kwargs)

def vote(request, ytid1 = None, ytid2 = None):
    if not request.session.session_key:
        request.session['created']=datetime.datetime.now().strftime(dateFormat)
    choices = {}
    choices['left'] =  getVideoMetadata()
    choices['vs'] = 'vs'
    choices['right'] =  getVideoMetadata()
    context = {'choices':choices}
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

def getVideoMetadata(ytid = None):
    ytJsonDir  = Path(r'C:\Users\Ryan\Desktop\Files\kingcobrajfs')
    videoJsons = [x for x in ytJsonDir.iterdir() if '.json' == x.suffix]
    if ytid:
        vidJson = [x for x in videoJsons if ytid in x.filename][0]
    else:
        #we select at random
        vidJson= random.choice(videoJsons)

    with open(vidJson) as j:
        """
        {'dislike_count': 23,
        'duration': 566,
        'like_count': 12,
        'thumbnail': 'https://i.ytimg.com/vi_webp/-GCPUBayK7E/maxresdefault.webp',
        'title': 'painting a wand',
        'webpage_url': 'https://www.youtube.com/watch?v=-GCPUBayK7E'}
        """
        ytInfo = json.load(j)    
        keepAttrs= ['id',
                    'title',
                    'thumbnail',
                    'like_count',
                    'dislike_count',
                    'view count',
                    'duration',
                    'webpage_url',
                    'upload date',
                    ]
        ytInfo = {k:v for k,v in ytInfo.items() if k in keepAttrs}
    return ytInfo
   
if __name__ == '__main__':
    print(findFile('LipcFI8tq_I', thumbnailExtensions))
    print(findFile('7H3VhvU_2Aw', thumbnailExtensions))
    #http://127.0.0.1:8000/vote/LipcFI8tq_I-7H3VhvU_2Aw

