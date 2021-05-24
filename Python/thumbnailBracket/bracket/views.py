from django.http import HttpResponse
from django.template import loader

from .models import Leaderboard, Vote, Thumbnail

from pathlib import Path
from configparser import ConfigParser

configPath = Path('C:/Users/Ryan/Desktop/Files/corpus/Python/thumbnailBracket/bracket/config.ini')
if not configPath.exists():
    raise FileNotFoundError('Config file not found')

config = ConfigParser()
config.read(configPath)
channelDir = Path(config['globals']['channelDirectory'])
thumbnailExtensions = {'webp','jpg'}

def findFile(ytid: str, extensions: set[str]) -> Path:
    for file in channelDir.iterdir():
        if (    file.is_file()
                and ytid in file.name
                and set(file.suffixes).intersection(extensions)):
            return file
    else:
        raise FileNotFoundError('Could not find ytid')

def index(request):
    return HttpResponse("Hello, world. You're at the index.")
    
def vote(request, ytid1, ytid2):
    try:
        left = findFile(ytid1, thumbnailExtensions)
        right = findFile(ytid2, thumbnailExtensions)
    except:
        left, right = None, None
    msg = (f"You're at the vote page. Video thumbnails {left} and {right} duke it out."
            "\n"
            f""
        )
    return HttpResponse(msg)

if __name__ == '__main__':
    print(findFile('LipcFI8tq_I', thumbnailExtensions))