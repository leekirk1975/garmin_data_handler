

from garminexport import garminclient as ge
import garminexport.incremental_backup as gcb

from garminconnect import Garmin as gc
import datetime
import pandas as pd
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')

def df_to_csv(data, fileName,date_stamp): #create csv file
   cwd = os.getcwd()#get the current working directory
   # Save all data files to a sub directory to aviod cultering
   csvname = cwd + '/data/'+ fileName+ '_' + str(date_stamp.strftime('%Y%m%d%H%M%S')) + '.csv'
   data.to_csv(csvname)



#set todays date
today = datetime.date.today()
start_date = datetime.date(2020, 11, 1)
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
#gcb.incremental_backup(email,pwd,backup_dir,("fit"))
#"fit","json_summary", "json_details", "gpx", "tcx"
client = ge.GarminClient(email,pwd)
ge.GarminClient.connect(client)
activity_fit = ge.GarminClient.get_activity_fit(client,5750722867)



##########################
#client = gc(email,pwd)
#gc.login(client)
#this picks up the power curve and the Vo2 max
#activities = gc.get_activities(client,0,20)
#fit = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
#csv = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.CSV)
#print (csv)


print(backup_dir  + '/test.fit')
with open(backup_dir + "/test.fit", mode="wb") as f:
    f.write(activity_fit)