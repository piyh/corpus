#this script is a massive overcomplication and shoudn't be used
import re
import os
import shlex, subprocess
from time import sleep
import sys

os.chdir('C:/kingcobrajfs')

global cachedProgress

jfsChannels = ('https://www.youtube.com/channel/UCkQTpXVcbssfgki1CN_bXCQ','https://www.youtube.com/user/KingCobraJFS')
youtubedlPath = r'C:\Users\Ryan\AppData\Local\Programs\Python\Python39\Scripts\youtube-dl.exe'
def finished(process):
    try:
        if process.returncode != 0:
            return False
        else:
            return True
    except (AttributeError, NameError) as e:
        return False
    
def main(channelURL):
    youtube_dl = ''
    #fails on Vid 549, 357, 607,681, 789,841, 894, 914, 931, 936, 956, 1073,1096, 1212, 1319
    startVid = 1
    dlQueueLen = -1 #initalizing values with -1, should never be doing useful logic with this value
    curVid = -1 
    sleepInterval = 3

    erroredVids = []
    while not finished(youtube_dl):
        curVid = 1
        
        youtubedlCmd = f'{youtubedlPath} --newline --write-auto-sub -v --playlist-start {startVid} {channelURL}'
        print(youtubedlCmd)
        youtubedlCmd = shlex.split(youtubedlCmd)
        print(youtubedlCmd)
        youtube_dl = subprocess.Popen(youtubedlCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = youtube_dl.communicate()
        out = out.decode(encoding='cp1252').split('\n') #encoding='cp1252' if on windows
        err = err.decode(encoding='cp1252').split('\n') #taking stdout/stderr from bytes to list of strings
        
        for line in out: #read stdout
            print(line)
            if '[download] 100%' in line:
                print(line)

            matchObj = re.match(r'\[youtube\] \w{11}: Downloading webpage', line)
            if matchObj:
                print(line)

            matchObj = re.match(r'\[download\] Downloading video (\d+) of (\d+)', line) #look to see which video we're on
            if matchObj:
                curVid = int(matchObj.group(1)) #get current vid
                dlQueueLen  = int(matchObj.group(2)) #get total vids undownloaded in playlist

        for line in err: #read stderr
            matchObj = re.match(r"^(?!(\[debug\]|WARNING: Couldn't find automatic captions))", line)
            if matchObj:
                print(line)

        print(f'youtube_dl.returncode:{youtube_dl.returncode}')

        startVid = startVid + curVid

        #if youtube_dl.returncode !=0:
        erroredVids.append(startVid-1)

        global cachedProgress
        cachedProgress = f'startVid:{startVid}, curVid:{curVid}, dlQueueLen:{dlQueueLen}, totalVids:{dlQueueLen + startVid}, erroredVids:{erroredVids}'
        
        print(cachedProgress)
        
        print(f'restarting youtube-dl at vid #{startVid}')

        #sleepInterval = sleepInterval + 30
        print(f'sleeping for {sleepInterval} seconds')
        sleep(sleepInterval)

    print(cachedProgress) 
    print("Exiting Main")

if __name__ == '__main__':
    global cachedProgress
    for channel in jfsChannels:
        try:
            main(channel)
        except KeyboardInterrupt:
            print(cachedProgress)
            try:
                sys.exit(128) # not sure if 128 does anything, too scared to change
            except SystemExit:
                os._exit(128)
input('press enter to exit')
