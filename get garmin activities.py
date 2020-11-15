

from garminexport import garminclient as ge
import garminexport.incremental_backup as gcb

from garminconnect import Garmin as gc
import datetime
import pandas as pd
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')


#write CSV files
def df_to_csv(data, fileName,date_stamp): #create csv file
   cwd = os.getcwd()#get the current working directory
   # Save all data files to a sub directory to aviod cultering
   csvname = cwd + '/data/'+ fileName+ '_' + str(date_stamp.strftime('%Y%m%d%H%M%S')) + '.csv'
   data.to_csv(csvname)


##########################Garminconnect
#client = gc(email,pwd)
#gc.login(client)
#this picks up the power curve and the Vo2 max
#activities = gc.get_activities(client,0,20)
#fit = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
#csv = gc.download_activity(client,5750722867,dl_fmt=client.ActivityDownloadFormat.CSV)
#print (csv)


#set todays date
today = datetime.date.today()
start_date = datetime.date(2020, 11, 1)


#set the location to store files
cwd = os.getcwd()
backup_dir = cwd + '/data/garmin_backup'
#write all files excluding fit - for some reason when this function is passed it fails "fit", the code block below adds the missing fit files
gcb.incremental_backup(email,pwd,backup_dir) #("json_summary", "json_details", "gpx", "tcx"))



''' get missing FIT files and write to the the directory passed'''
#login to garmin
client = ge.GarminClient(email,pwd)
ge.GarminClient.connect(client)

#get  list of all garmin activities
activity_list = ge.GarminClient.list_activities(client)

#this works for opening fit files. using garmin export
#create a fit file for the active file passed and then write it the directory passed.
activity_fit = ge.GarminClient.get_activity_fit(client,5817728933)
print(backup_dir  + '/5817728933.fit')
with open(backup_dir + "/5817728933.fit", mode="wb") as f:
    f.write(activity_fit)