import random
from pathlib import Path
from configparser import ConfigParser
import json
from pprint import pformat
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote
from .common import config, channelDir, thumbnailExtensions, logger, intersperse
from django.urls.resolvers import LocalePrefixPattern #urlencode, 

try:
    from .models import Leaderboard, Vote, Thumbnail
except:
    print('got import errors when importing models')
    #TODO: remove block, keep import
    pass


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
    #template = loader.get_template('polls/index.html')
    #context = {'left':'Datong is not a social Statis-LipcFI8tq_I.webp'}
    
def vote(request, ytid1 = None, ytid2 = None):

    
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
        response = render(request, 'voteContainer.html', context)
    return response  

    if request.method == 'GET':
        context = {'left':quote('Datong is not a social Statis-LipcFI8tq_I.webp'),
                'left_ytid': 'LipcFI8tq_I',
                'right':quote('Taco Jhon’s Boss Burito review-7H3VhvU_2Aw.webp'),
                'right_ytid':'7H3VhvU_2Aw',
                    }
        try:
            left = findFile(ytid1, thumbnailExtensions)
            right = findFile(ytid2, thumbnailExtensions)
            context['left_friendly'] = left.name[:- len(left.suffix) - len('-ytidXXXXXXX')]
            context['right_friendly'] = right.name[:- len(right.suffix) - len('-ytidXXXXXXX')]
        except:
            left, right = None, None
        msg = (f"You're at the vote page. Video thumbnails {left} and {right} duke it out."
                "\n"
                f""
            )
        return render(request, 'vote.html',context)#HttpResponse(msg)

def get_client_ip(request):
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

