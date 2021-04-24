from pathlib import Path
from pprint import pprint as pp
moveFrom = Path(r'C:\Users\Ryan\Desktop\Files\code\Rpi\chicam')
dest = Path(r'C:\Users\Ryan\Desktop\Files\code\Rpi\camera')
duped = Path(r'C:\Users\Ryan\Desktop\Files\code\Rpi\camera\duped')
if not duped.exists: duped.mkdir()

moved=0
for moveFile in moveFrom.glob('**/*'):
    if moveFile.is_file() and moveFile.suffix in ('.mkv','.h264'):
        workingSize = moveFile.stat().st_size
        destName = dest.joinpath(moveFile.name)
        if not destName.exists():
            moveFile.rename(destName)
            moved+=1
        else:
            if destName.stat().st_size == workingSize:
                print(f'sameSize:{workingSize}, \n\t{destName=}, \n\t{moveFile=}\n\tdeleting{moveFile}')
                moveFile.unlink()
            else:
                dupeFolderFile = duped.joinpath(moveFile.name)
                if not dupeFolderFile.exists():
                    moveFile.rename(dupeFolderFile)
                else:
                    print(f'skipped {moveFile=}')
    else:
        if moveFile.is_dir():
            if len([x for x in moveFile.iterdir()]) ==0 and '.git' not in str(moveFile):
                print(f'removing empty dir {moveFile}')
                moveFile.rmdir()
                
print(moved)
