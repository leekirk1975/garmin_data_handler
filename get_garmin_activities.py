"""Export activities from garmin that are not in the dir, in all formats (json, gpx, tcx, FIT)"""

import garminexport.incremental_backup as gcb
import os
from fake_useragent import UserAgent


#created a randam user agent
#For library clients, one can pass a user_agent_fn function that, when called, produces a
#User-Agent string to be used as User-Agent for the remainder of the session.
def gen_user_agent():
    ua = UserAgent()
    return ua.random

print("logging on")
# get login and password
email, pwd = open('GarminDetails.txt').read().strip().split(',')



"""Use Garminexport to export all activity history from garmin connect, 
then set the location and copy all files to this location"""
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
# write all files types to the back-up directory - Json, gpx, tcx and FIT
print(backup_dir)
print('writing back-up files')
gcb.incremental_backup(email, pwd, gen_user_agent, backup_dir)
print('all done')
