word_list = ['hi','there','general','kenobi']
word = ['hi','there']

import os, os.path as path
os.chdir("E:\\kingcobrajfs")

wordList =[]

with open('wordlist_remove.txt', 'r') as words:
    for line in words:
        wordList.append(line.strip())

with open('workfile', 'r') as inbound:
    readFile = ""
    for line in inbound:
        readFile = readFile + ' ' + line.strip() + ' \n \n' 

with open('workfileUnique', 'w') as outbound:
    outbound.write(' \n'.join([i for i in readFile.split() if i not in wordList]))

print('done')
