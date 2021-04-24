import os
from pathlib import Path

ytBase = 'https://www.youtube.com/watch?v='

subtitleDir = Path('E:/kingcobrajfs')

ytIDs = [{x.name[-len('7CzPBMbQJrA.en.vtt'):-len('.en.vtt')]:x.name[:-len('-7CzPBMbQJrA.en.vtt')]} for x in subtitleDir.iterdir() if '.vtt' in x.name]


with open('cobralinks.txt','w') as f:
    for ytID in ytIDs:
        for entry in ytID.items():
            f.write(ytBase + entry[0] + '  - ' + entry[1] + '\n')
#        f.write(str(ytID))

print(ytIDs[0])
