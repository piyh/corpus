from pathlib import Path
from configparser import ConfigParser
import logging
import sys 

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

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x