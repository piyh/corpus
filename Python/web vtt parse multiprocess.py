import os, os.path as path
from datetime import datetime 
from pathlib import Path
import webvtt

os.chdir("C:/Users/Ryan/Desktop/Files/kingcobrajfs")

lastCap = ""
minuteCache = 0

targetVTT = ''
findString = 'ripping ass'
fileList = [name for name in os.listdir('.') if os.path.isfile(name) and ".vtt" in name and targetVTT in name]
#for vtt in fileList:
with open('transcript', 'w') as f:


#TODO: make this a function that returns a list of strings that is a markup formatted link with youtube ID, title, timestamp, text and link
def parseVtt(vtt):
        vttName = vtt
        vtt = path.join(os.getcwd(), vtt)
        vttPath = Path(os.getcwd()).joinpath(vtt)
        f.write(vtt + '\n')
        for c,caption in enumerate(webvtt.read(vtt)):
            text = caption.text.replace('\n',' ').strip()
            
            hour = caption.start[0:2]
            minute = caption.start[3:5]
            second = caption.start[6:8]
            videoID = vttName[-18:-7]

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
            ctime = datetime.fromtimestamp(vttPath.stat().st_ctime)
            if findString in caption.text:# and ctime.year == 2020 and ctime.month in (7,8):#' pill ' in caption.text:
                #hour = caption.start[0:2]
                #minute = caption.start[3:5]
                #second = caption.start[6:8]
                #videoID = vttName[-18:-7]
                print(f'[{caption.text}](https://www.youtube.com/watch?v={videoID}&t={hour}h{minute}m{second}s)')
                print('\n')

            if int(minute) % 2 ==0 and minute != minuteCache:
                f.write('\n')
                f.write(caption.start[:5])
                f.write('\n')
                minuteCache = minute
            
            f.write(' ')
            
        f.write('\n')
               


