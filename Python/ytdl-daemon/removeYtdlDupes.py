import os
#from collections import Counter
#import pandas as pd
from pathlib import Path
from datetime import datetime
from pprint import pprint as pp

def returnDupes(li):
    seen = set()
    dupe = set()
    for ele in li:
        if ele not in seen:
            seen.add(ele)
        else:
            dupe.add(ele)
    return dupe

i = input('type delete to disable dry run')
dryRun = ('delete' != i)

wd = Path(r'C:\Users\Ryan\Desktop\Files\kingcobrajfs')
os.chdir(wd)

videos = []
ids = []

extensionGroup = ('.mkv', '.webm', '.mp4')

for file in wd.iterdir():
    """extension group is a group you want to dedupe from
    for exmaple if you want keep only one picture called dog, and have dog.jpg and dog.png, 
    this function will delete the newer one
    """
    ext = file.suffix
    lenSuffixes = sum([len(x) for x in file.suffixes])
    if ext in extensionGroup:
        ytID = file.name[len(file.name)-lenSuffixes-11:-lenSuffixes] #11 is youtube id len
        ids.append(ytID)
        videos.append({'ytID':ytID #could merge the dupe dictValue append logic with this, but performance doens't matter and I don't want to rewrite
                       , 'path':file
                       , 'size':file.stat().st_size
                       , 'mtime':file.stat().st_mtime})

dupeSet = returnDupes(ids)

dupeDict = {}
for file in videos:
    if file['ytID'] in dupeSet:
        ytID = file['ytID'] 
        appendValues = {'path':file['path'], 'mtime':file['mtime']}
        dictValue = dupeDict.get(ytID)
        if dictValue:
            dictValue.append(appendValues)
            dictValue.sort(key = lambda x: x.get('mtime'))
            deleting = dictValue[0]
            saving = dictValue[1]
            print(deleting)
            print(saving)
            if dryRun:
                print(f"dry run: would have deleted {deleting.name} as it's older than {saving.name}")
            else:
                print(f"deleting {deleting['path'].name} as it's older than {saving['path'].name}")
                dictValue[0]['path'].unlink()
            del dictValue[0]
        else:
            dupeDict[ytID] = [appendValues]

input('press enter to exit')
