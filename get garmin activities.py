

import garminexport.incremental_backup as gcb
from garminconnect import Garmin as gc
import datetime
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')

#set the location to store files
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
#write all files types to the back-up directory - Json, gpx, tcx and FIT
gcb.incremental_backup(email,pwd,backup_dir)



##########################Garminconnect
#client = gc(email,pwd)
#gc.login(client)
#this picks up the power curve and the Vo2 max
#activities = gc.get_activities(client,0,20)
#fit = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
#csv = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.CSV)
#print (csv)

