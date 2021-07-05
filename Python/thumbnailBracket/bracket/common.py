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
if configPath.exists():
    config = ConfigParser()
    config.read(configPath)
    channelDir = Path(config['globals']['channelDirectory'])
else:
    channelDir = Path('/mnt/videoMetadata')
    if not channelDir.exists():
        raise FileNotFoundError(f'{channelDir.filename} dir not found')
    children = [x for x in channelDir.iterdir()]
    if not children:
        raise Exception(f'no metadata found in {channelDir.filename}, did you remember to mount the info jsons from youtube-dl?')


#thumbnailExtensions = {'.webp','.jpg'}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('django.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

ytJsonDirs  = (Path(r'C:\Users\Ryan\Desktop\Files\kingcobrajfs'),Path('/mnt/videoMetadata'))
ytJsonDir = [x for x in ytJsonDirs if x.exists()][0]
logger.debug(ytJsonDir)

def getEqualPlayData():
    """
    returns a list of 
        dbRec(ytid='K5PEo1p0Nug', voteCount=6, winCount=4)
    """
    normalizedVoteCols = """ ytid,
                            opponentYtid,
                            outcome,
                            voteDatetime,
                            session,
                            postingIp"""
    try:
        sqlCols = 'ytid voteCount winCount'
        sql = """select 
                      ytid
                     ,count(*) as voteCount
                     ,sum(case outcome when 'win' then 1 else 0 end) as winCount
                  from normalizedVotes 
                  group by ytid 
                  order by count(*)
                    ,sum(case outcome when 'win' then 1 else 0 end)
                    ,RANDOM();"""
        results=runSql(sql, None, sqlCols)
        #if not results:
            #raise RuntimeError("no results returned")
        return(results)

    except Exception as e:
        print('EXCEPTION!!!- ' + str(e))
        sql = "drop view if exists normalizedVotes;"
        runSql(sql)
        sql =  ( "create view  normalizedVotes (\n"
                f'{normalizedVoteCols}\n'
                ') as \n'
                'select winYtid,\n'
                "    loseYtid,\n"
                "    'win',\n"
                "    substr(voteDatetime, 0, 19),\n"
                "    session,\n"
                "    postingIp\n"
                "from bracket_vote \n"
                "union all \n"
                "select loseYtid, \n"
                "    winYtid, \n"
                "    'loss', \n"
                "    substr(voteDatetime, 0, 19), \n"
                "    session, \n"
                "    postingIp \n"
                "from bracket_vote;"
        )
        runSql(sql)

def getVoteOption() -> dict:
    """
    TODO: make this a fair choice, don't let randomness allow a picture to get more votes than others through chance
    """
    ytids = list(metadataByYtid.keys())
    
    votes = getEqualPlayData()
    voteIDs = [x.ytid for x in votes]
    unvotedIDs = set(ytids) - set(voteIDs)
    if unvotedIDs:
        return metadataByYtid[random.choice(list(unvotedIDs))]
    else:
        weightedChoice = random.randint(0,int(len(votes)*.1))
        ytid = votes[weightedChoice].ytid
        return metadataByYtid[ytid]
    #rando = random.choice(ytids)
    #return rando
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

def getMetadataByYtid(metadataByYtid={}):
    """
    if passed metadata, just do an update for new info jsons, otherwise get all metadata
    """
    return 'derp'


metadataByYtid = getAllMetadata(ytJsonDir)        

def addVoteDataToMeta(metadata:dict) -> dict:
    """
        TODO: returns a new metadataByYtid dict with vote info added
    """
    eqpData = getEqualPlayData()
    metadataYtidsSet = set(metadataByYtid.keys())
    voteSet     = set([x.ytid for x in eqpData])
    for metadata in metadataByYtid:
        #if metadata['']

        metadata['votes'] = 0
        metadata['wins'] = 0

def addMatchHistoryMetadata(metadata:dict, fullHist:bool = False) -> dict:
    """adds matchHistory key to metadata if fullHist =True
         - list of namedTuple with cols 'ytid opponentYtid outcome voteDatetime session postingIp' 
       
        if not fullHist, just does win ratio

       also adds winRatio directy to metadata
    """
    columns  = 'ytid opponentYtid outcome voteDatetime session postingIp'
    wins     = runSql("select winYtid, loseYtid, 'win', substr(voteDatetime,0,19), session, postingIp from bracket_vote where winYtid=:ytid limit 10;"
                        ,{'ytid':metadata['id']}
                        ,columns
                )
    losses   = runSql("select loseYtid, winYtid, 'loss', substr(voteDatetime,0,19), session, postingIp from bracket_vote where loseYtid=:ytid limit 10;"
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
    def vidLength (x):
        totalSecs = int(x)
        h = totalSecs//3600
        if h>1:
            hText=f'{h} hours'
        elif h==1:
            hText=f'{h} hour'
        else:
            hText=''
        m = (totalSecs%3600) // 60
        if m>1:
            mText=f'{m} minutes'
        elif m==1:
            mText=f'{m} minute'
        else:
            mText=''
        #sec =(totalSecs%3600)%60 #just for reference
        return f'{hText} {mText}'
    infoTableMap = {
        'upload_date':{
            'displayName':'Uploaded',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y%m%d').strftime(dateFormat),
        },
        'duration':{
            'displayName':'Length',
            'transformFunction': vidLength #lambda x: datetime.timedelta(seconds=x)
        },
        'view_count':{
            'displayName':'Views',
            'transformFunction': lambda x: "{:,}".format(int(x))
        },
        'webpage_url':{
            'displayName':'link',
            'transformFunction': lambda x: f'<a href="{x}" target="_blank">!-----!</a>',
        },
        'voteDatetime':{
            'displayName':'Vote Time',
            'transformFunction': lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime(datetimeFormat),
        },
        #'winRatio':{ #TODO: this is a test line in the infoTable
        #    'displayName':'Stats/Win/Loss/%',
        #    'transformFunction': lambda x: f'<a href="/stats/{metadata.id}" target="_blank">Stats - </a>',
        #},
    }
    displayDict = {}
    print(metadata)
    for k,v in metadata.items():
        if k == 'title':
            title = v
            continue
        if not infoTableMap.get(k):
            continue
        displayName = infoTableMap[k]['displayName']          

        transform    = infoTableMap[k].get('transformFunction')
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
        displayDict['Stats/Wins/Losses/%'] = (f"<a href='/stats/{metadata['id']}' target='_blank'>Stats</a> - "
                                        f"<span class='text-success'>{metadata['wins']}</span>"
                                        f"/<span class='text-danger'>{metadata['losses']}</span>"
                                        f"/{metadata['winRatio']}"
                                        
        )

    return displayDict

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