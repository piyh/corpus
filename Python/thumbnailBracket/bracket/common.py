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
        "view_count": 1993,
        "upload_date": "20170427",
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
            metadatum = json.load(j)    
        ytid = metadatum['id']
        metadatum = {k:v for k,v in metadatum.items() if k in keepAttrs}
        metadataCollection[ytid] = metadatum
    return metadataCollection

def getRandYtidMeta() -> dict:
    metadataYtids = list(metadata.values())
    rando = random.choice(metadataYtids)
    return rando

metadata = getAllMetadata(ytJsonDir)        
