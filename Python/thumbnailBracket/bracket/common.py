#from .common import config, channelDir, thumbnailExtensions, logger, intersperse
from pathlib import Path
from configparser import ConfigParser
import logging
import random
import sys 
import json

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

ytJsonDir  = Path(r'C:\Users\Ryan\Desktop\Files\kingcobrajfs')

def getAllMetadata(ytJsonDir: Path) -> dict:
    """
    returns a dict with many records like this
    {'-GCPUBayK7E':
        {'dislike_count': 23,
        'duration': 566,
        'like_count': 12,
        "view count": 1993,
        "upload date": "20170427",
        'thumbnail': 'https://i.ytimg.com/vi_webp/-GCPUBayK7E/maxresdefault.webp',
        'title': 'painting a wand',
        'webpage_url': 'https://www.youtube.com/watch?v=-GCPUBayK7E'}
    }
    """
    metadataCollection = {}
    keepAttrs = ['id',
                'title',
                'thumbnail',
                'like_count',
                'dislike_count',
                'view_count',
                'duration',
                'webpage_url',
                'upload_date',
                ]
    for infoJson in ytJsonDir.iterdir():
        if not '.json' == infoJson.suffix:
            continue
        with open(infoJson) as j:
            metadata = json.load(j)    
        #metadata = {k:v for k,v in metadata.items() if k in keepAttrs} #k.replace(' ','_')
        ytid = metadata['id']
        metadataCollection[ytid] = metadata
    return metadataCollection

metadata = getAllMetadata(ytJsonDir)        
metadataYtids = list(metadata.values())
ytids = [x for x in metadata.keys()]

random.shuffle(ytids)

def getRandYtidMeta() -> dict:
    rando = random.choice(metadataYtids)
    return rando

'''
def getVideoMetadata(ytid:list[str] = None, numChoices:int = 2) -> dict: 
    """
    DO NOT USE
    reads the global jsonQueue
    returns a metadata dict 
    if ytid not populated, gets random off disk
    """
    global jsonQueue
    if ytid:
        vidJson = [x for x in ytJsonDir.iterdir() if ytid in x.name and '.json' == x.suffix][0]
    else:
        #we select at random, but refresh the video jsons if the list shrinks too much
        if len(jsonQueue) > numChoices:
            jsonQueue = [x for x in ytJsonDir.iterdir() if '.json' == x.suffix]
            random.shuffle(jsonQueue)    
        vidJson = jsonQueue.pop()

    with open(vidJson) as j:
        """
        {'dislike#_count': 23,
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
        ytInfo = {k.replace(' ','_'):v for k,v in ytInfo.items() if k in keepAttrs}
    return ytInfo
'''


"""def findFile(ytid: str, extensions: set[str]) -> Path:
    for file in channelDir.iterdir():
        if (    file.is_file()
                and ytid in file.name
                and set(file.suffixes).intersection(extensions)):
            return file
    else:
        logger.exception(f"couldn't {ytid} with extensions {extensions}")
        raise FileNotFoundError('Could not find ytid')
"""


#@dataclass
#class ytVid:
#    id: str
#    title: str
#    thumbnail: str
#    like_count: int
#    dislike_count: int
#    view_count: int
#    duration: int
#    webpage_url: str
#    upload_date: str