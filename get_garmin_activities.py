# Export activities from garmin that are not in the dir, in all formats (json, gpx, tcx, FIT)
import garminexport.incremental_backup as gcb
# from garminconnect import Garmin as gc
# import datetime
import os

# get login and password
print("logging on")
email, pwd = open('GarminDetails.txt').read().strip().split(',')
#######################################################
# Use Garminexport to export all activity history
# set the location to store files
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
# write all files types to the back-up directory - Json, gpx, tcx and FIT
print(backup_dir)
print('writing back-up files')
gcb.incremental_backup(email, pwd, backup_dir)
print('finished')
#######################################################
