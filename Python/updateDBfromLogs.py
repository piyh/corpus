import re
import sqlite3
import shutil
from datetime import datetime
import time

cleanData = []

rawLogFile = 'ongoinglogs.txt' #parameterize python script for these values
rawLogsArchive = 'httpMapArchive'
con = sqlite3.connect('nginxlogs.db')

with open (rawLogFile) as log:

#parse regex, returns list of tuples with parsed httplog info
def parseRegex(nginxLog):
	parsedData = []
	monthDict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07', \
		'Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

	for line in nginxLog:
		line = line.replace('|','') #pull pipes out of data, not sure if needed anymore
		row = re.findall( \
			'^(\d+?\.\d+?\.\d+?\.\d+).+?(\d+?)/([a-zA-Z]{1,3})/(\d{4}):(.{8}).*?"(.*?)"\s\d+\s\d+\s"(.*?)"\s"(.*?)"' \
			,line)[0] 
#		parsedData.append(regexGroups)
#	for row in parsedData:
		event = row[0], row[5], row[6], row[7], row[3] + '-' + monthDict.get(row[2]) + '-' \
			+ row[1] + 'T' + row[4]
		insertData.append(event)
#insert formatted data into sqlite
def sqliteInsert(insertData): #takes list of tuples and inserts into DB
	for row in insertData:
		con.execute("insert into httplogs (ip, request, referrer, agent, timestamp,imported) " + \
                        "values (?,?,?,?,?,0)",row)
	con.commit()

#do this in a loop, read log file, parse it and insert into DB while keeping position
while True:#some condition
	where log.tell()
	x = log.readline()
	if x:
		#regex parse it
		#drop it in DB
	else:
		time.sleep(60)
		log.seek(where) # do i need this?
	#end loop


#move file to archive after loading
#shutil.move(rawLogFile, rawLogsArchive + '/' +rawLogFile + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.processed')

