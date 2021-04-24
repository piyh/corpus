from pathlib import Path
import os

jfsDir = Path('D:/kingcobrajfs')

vtts = [x.name for x in jfsDir.iterdir() if '.vtt' in x.name]
print(len(vtts))
os.chdir(jfsDir)

countWand = 0
for vtt in vtts:
        with open (vtt, 'r') as f:
                li = f.readlines()
                for line in li:
                        countWand = count +  line.count('wand')
print(count)
