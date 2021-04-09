from pathlib import Path
import threading
import json
from collections import defaultdict
from pprint import pprint, pformat
import time
import logging

dupeSearchStart = time.time()
#compare by file attributes, basically just size and name, then by hash if same name/size
#if name/size disagree, put in a conflict csv to review later
outputDir = Path(r'C:\Users\Ryan\Desktop')
directories = (r'C:\Users\Ryan\Desktop',
               #r'D:\Users\Ryan',
               'G:\\',
               'F:\\',
               #'H:\\',
               )
directories = [Path(x) for x in directories]
excludeDirs = {'$RECYCLE.BIN',
               'gdpr data',
               'steamapps',
               'Google Dump',
                   }

nameSet = set()
files = []
dupeDict = defaultdict(list)
for wd in directories:
    dirDupeSearchStart = time.time()
    for file in wd.glob('**/*'):
        if file.is_file() and not excludeDirs.intersection(set(file.parts)):
            fileDict = {#'name':file.name,
                        'path':file.as_posix(),
                        'size':file.stat().st_size,
                        'mtime':file.stat().st_mtime,
                        }
            try:
                dupeDict[file.name].append(fileDict)
            except:
                logging.exception(f"couldn't add this filedict, continuing \n {fileDict}")
                raise
    print('len of files parsed = ', len(dupeDict))
    print(f'processed {wd} in {time.time() - dirDupeSearchStart}s')

uniqueDict = {k:v for k,v in dupeDict.items() if len(v) == 1}
print('number of uniques = ', len(uniqueDict))
dupeDict   = {k:v for k,v in dupeDict.items() if len(v) > 1}
print('number of dupes = ', len(dupeDict))

writingStart = time.time()
print('writing to file')    
with open(outputDir.joinpath('duplicateFiles.json'),'w',encoding='utf8') as f:
    json.dump(dupeDict, f, indent = 1 )
    
with open(outputDir.joinpath('uniqueFiles.json'),'w',encoding='utf8') as f:
    json.dump(uniqueDict, f, indent = 1 )
print(f'done writing to file, took {time.time() - writingStart}s')
print(f'finished script in {time.time() - dupeSearchStart}s')

"""
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
"""
