

from garminexport import garminclient as gc
import garminexport.incremental_backup as gcb
import datetime
import pandas as pd
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')

#set todays date
today = datetime.date.today()

cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
gcb.incremental_backup(email,pwd,backup_dir,'ALL', False,7)


