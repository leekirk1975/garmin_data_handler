

from garminexport import garminclient as gc
import garminexport.incremental_backup as gcb
import datetime
import pandas as pd
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')

#set todays date
today = datetime.date.today()



client = gcb.GarminClient(email,pwd)
gcb.GarminClient.connect(client)
gcb.incremental_backup()


