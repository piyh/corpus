from pathlib import Path
from configparser import ConfigParser
import logging
import random
import sys 
import json
import sqlite3
from collections import namedtuple
import datetime

dateFormat = '%Y-%b-%d'
datetimeFormat = '%Y-%b-%d %H:%M:%S'

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

#metadata should be an object and these functions should be an object too
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
    metadataByYtid = {}
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
        ytid = metadata['id']
        metadata = {k:v for k,v in metadata.items() if k in keepAttrs}
        metadataByYtid[ytid] = metadata
    return metadataByYtid

metadataByYtid = getAllMetadata(ytJsonDir)        

def addMatchHistoryMetadata(metadata:dict, fullHist:bool = False) -> dict:
    """adds matchHistory key to metadata if fullHist =True
         - list of namedTuple with cols 'ytid opponentYtid outcome voteDatetime session postingIp' 
       
        if not fullHist, just does win ratio

       also adds winRatio directy to metadata
    """
    columns  = 'ytid opponentYtid outcome voteDatetime session postingIp'
    wins     = runSql("select winYtid, loseYtid, 'win', substr(timestamp,0,19), session, postingIp from bracket_vote where winYtid=:ytid"
                        ,{'ytid':metadata['id']}
                        ,columns
                )
    losses   = runSql("select loseYtid, winYtid, 'loss', substr(timestamp,0,19), session, postingIp from bracket_vote where loseYtid=:ytid"
                        ,{'ytid':metadata['id']}
                        ,columns
                )
    if losses:
        matchHistory = (wins + losses)
        winRatio = float(len(wins)) / len(matchHistory)
    else:
        matchHistory = wins
        winRatio = float(len(wins))
    
    metadata['wins']   = len(wins)
    metadata['losses'] = len(losses)

    winRatio  *= 100
    winRatio   = str(int(winRatio)) + '%'

    metadata['winRatio']     = winRatio

    if fullHist:
        print('in full hist mode')
        matchHistory.sort(key = lambda x: [0])
        metadata['matchHistory'] = matchHistory
    return metadata

def metadataDisplayMap(metadata:dict) -> dict:
    """takes an info json and returns a new display values dict to be paired with the metadata dict

    works with the ytVidMetaTable.html include"""
    infoTableMap = {
        'upload_date':{
            'displayName':'Uploaded',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y%m%d').strftime(dateFormat),
        },
        'duration':{
            'displayName':'Length',
            'transformFunction': lambda x: datetime.timedelta(seconds = x),
        },
        'view_count':{
            'displayName':'Views',
        },
        'webpage_url':{
            'displayName':'link',
            'transformFunction': lambda x: f'<a href="{x}" target="_blank">!-----!</a>',
        },
        'voteDatetime':{
            'displayName':'Vote Time',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime(datetimeFormat),
        },
    }
    displayDict = {}
    for k,v in metadata.items():
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
    
    if metadata['dislike_count']:
        likeRatio = float(metadata['like_count'])/(float(metadata['like_count']) + float(metadata['dislike_count']))
    else:
        likeRatio = metadata['like_count']
    
    likeRatio *= 100
    likeRatio  = str(int(likeRatio)) + '%'

    displayDict['Likes/Dislikes/%'] = (f"<span class='text-success'>{metadata['like_count']}</span>"
                                       f"/<span class='text-danger'>{metadata['dislike_count']}</span>"
                                       f"/{likeRatio}"
    )
    #after transforming the display value, make the anchor inner text be the video title
    displayDict['link'] = displayDict['link'].replace('!-----!',title)

    if metadata.get('winRatio'):
        displayDict['Wins/Losses/%'] = (f"<span class='text-success'>{metadata['wins']}</span>"
                                        f"/<span class='text-danger'>{metadata['losses']}</span>"
                                        f"/{metadata['winRatio']}"
        )

    return displayDict

def getVoteOption() -> dict:
    """
    TODO: make this a fair choice, don't let randomness allow a picture to get more votes than others through chance
    """
    ytids = list(metadataByYtid.values())
    rando = random.choice(ytids)
    return rando

def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def runSql(sql:str, bindVariables:list = None, tupleLabels:str = '') -> list:
    """
    runs sql that should be read only against the django sqlite db.  
    Can take bind variables in the standard sqlite3 module styles.
    tupleLabels is optional and is a space delimited list
    """
    with sqlite3.connect('db.sqlite3') as con:
        if tupleLabels:
            def namedtuple_factory(cursor, row):
                dbRec = namedtuple('dbRec', tupleLabels)
                return dbRec(*row)
            con.row_factory = namedtuple_factory
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