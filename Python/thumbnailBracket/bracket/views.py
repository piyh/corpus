from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote #urlencode, 

try:
    from .models import Leaderboard, Vote, Thumbnail
except:
    print('got import errors when importing models')
    #TODO: remove block, keep import
    pass

from pathlib import Path
from configparser import ConfigParser
import logging
import sys
from pprint import pformat

configPath = Path('C:/Users/Ryan/Desktop/Files/corpus/Python/thumbnailBracket/bracket/config.ini')
if not configPath.exists():
    raise FileNotFoundError('Config file not found')

config = ConfigParser()
config.read(configPath)
channelDir = Path(config['globals']['channelDirectory'])
thumbnailExtensions = {'.webp','.jpg'}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('django.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)


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
    
    
def vote(request, ytid1, ytid2):
    #template = loader.get_template('bracket/index.html')
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

def result(request):
    if request.method == 'POST':
        logger.debug(dict(request.POST))
        return HttpResponse(pformat(dict(request.POST)).replace('\n','<br/>'))


if __name__ == '__main__':
    print(findFile('LipcFI8tq_I', thumbnailExtensions))
    print(findFile('7H3VhvU_2Aw', thumbnailExtensions))
    #http://127.0.0.1:8000/vote/LipcFI8tq_I-7H3VhvU_2Aw