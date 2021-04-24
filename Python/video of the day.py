from pathlib import Path
from datetime import datetime
import random

jfsDir = Path('D:/kingcobrajfs')

now = datetime.now()
found = []
for file in jfsDir.iterdir():
    ext = file.suffix
    #lenSuffixes = sum([len(x) for x in file.suffixes])
    if ext in ('.mkv', '.webm', '.mp4'):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)      
        if mtime.month == now.month and mtime.day == now.day:
            print(mtime.strftime('%Y-%b-%d'))
            print(file)
            found.append(file)
if not found:
    print('nothing uploaded this day/month in archives')
	
files = [x for x in jfsDir.iterdir() if 'vtt' not in x.name]
random.shuffle(files)
print(f'random video of the day is {files[0]}')

input('''
press enter to exit
press anything followed by enter to rerun
''')