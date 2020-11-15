

import garminexport.incremental_backup as gcb
from garminconnect import Garmin as gc
import datetime
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')


#######################################################
#Use Garminexport to export all activity history
#set the location to store files
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
#write all files types to the back-up directory - Json, gpx, tcx and FIT
gcb.incremental_backup(email,pwd,backup_dir)
#######################################################



