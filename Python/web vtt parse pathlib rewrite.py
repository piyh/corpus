import os, os.path as path
from datetime import datetime 
from pathlib import Path
import webvtt

jfsDir = Path("D:/kingcobrajfs")
#os.chdir("D:/kingcobrajfs")

lastCap = ""
minuteCache = 0

targetVTT = ''
findString = 'car crash'
fileList = [file for file in jfsDir.iterdir() if file.exists() and ".vtt" in file.name and targetVTT in file.name]

#TODO: create multiprocess for each vtt
#fileDict = { file.name[-18:-7]: {'vtt':file} for file in jfsDir.iterdir() if file.exists() and ".vtt" in file.name and targetVTT in file.name}
fileDict = {}
for file in jfsDir.iterdir():
    suffixesLen = sum([len(suffix) for suffix in file.suffixes])
    ytIdLen = 11
    ytId = file.name[-suffixesLen-ytIdLen : -suffixesLen]
    if fileDict.get(ytId) is None:
        fileDict[ytId] = {}
    if ".vtt" in file.name:
        fileDict[ytId]['vtt'] = file
    elif ".vtt" not in file.name and '.part' not in file.name:
       fileDict[ytId]['file'] = file

delKeys = []
for key in fileDict:
    if fileDict[key].get('vtt') is None or fileDict[key].get('file') is None:
        delKeys.append(key)

for key in delKeys:
    del fileDict[key]

#fileDict = { file.name[-18:-7]: {'vtt':file} for file in jfsDir.iterdir() if file.exists() and ".vtt" in file.name and targetVTT in file.name}

#fileDict = {for key, value in fileDict.keys() if ".vtt" not in file.name}
'''updatedFileDict = {}
for key, value in fileDict.items():
    for file in jfsDir.iterdir(): #non performant inner loop, doesn't matter unless i'm looking at 10s of thousands of vids
        if ".vtt" not in file.name and '.part' not in file.name and key in file.name:
            updatedFileDict[key] = {'vtt':fileDict[key]['vtt'], 'file':file}
'''
print('got updated dict')

#fileDict = updatedFileDict
#print(fileDict)
print(len(fileDict))

for id in fileDict:
    vtt = fileDict[id]['vtt']
    #vttName = vtt.name

    mtime = datetime.fromtimestamp(fileDict[id]['file'].stat().st_mtime)
    #print(id) 
    #if mtime.year == 2020 and mtime.month in (7,8):
        #print(mtime, fileDict[id]['file'])

    for c,caption in enumerate(webvtt.read(str(vtt))):
    
        text = caption.text.replace('\n',' ').strip()
        
        hour = caption.start[0:2]
        minute = caption.start[3:5]
        second = caption.start[6:8]
        videoID = vtt.name[-18:-7]

        if findString in caption.text:
            #hour = caption.start[0:2]
            #minute = caption.start[3:5]
            #second = caption.start[6:8]
            #videoID = vttName[-18:-7]
            print(f'[{caption.text}](https://www.youtube.com/watch?v={videoID}&t={hour}h{minute}m{second}s)')
            print('\n')

if True:
    exit()

with open('transcript', 'w') as f:
    for vtt in fileList:
        #vttName = vtt.name
        f.write(vtt.name + '\n')
        for c,caption in enumerate(webvtt.read(str(vtt))):
            text = caption.text.replace('\n',' ').strip()
            
            hour = caption.start[0:2]
            minute = caption.start[3:5]
            second = caption.start[6:8]
            videoID = vtt.name[-18:-7]

            if text == '':
                continue

            index = text.rfind(lastCap)
          
            if index ==0 and len(text) != len(lastCap):# partial 
                #vtt will keep part of the last spoken sentence in the next scheduled caption
                #I'm only grabbbing the new part of the caption with the newPortion variable
                newPortion = text[len(lastCap)+1:]
                #print(newPortion)
                f.write(newPortion)
                #make the last caption the new portion we sliced
                lastCap = newPortion
            elif index == -1 or c == 0: #last caption not found, print all of this new line
                #print(text)
                f.write(text)
                lastCap = text
            elif len(text) == len(lastCap) and index == 0:#ignore the line, exact dupe of last line
                pass
            else: #catchall, just print
                #print(f'PASSED----vtt:{vtt}, index:{index}, lastCap:{lastCap}, text:{text}')
                #print(text)
                f.write(text)
                lastCap = text
                pass
            #look for word/phrase and link to timestamp

            if int(minute) % 2 ==0 and minute != minuteCache:
                f.write('\n')
                f.write(caption.start[:5])
                f.write('\n')
                minuteCache = minute
            
            f.write(' ')
            
        f.write('\n')
               
            #[print(str(caption)[26:])  for caption in webvtt.read(vtt) if '\n' in str(caption)]
