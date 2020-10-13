

import garminexport
import garminconnect as gc
from datetime import date 

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = date.today()

client = gc.Garmin(email,pwd)
gc.Garmin.login(client)

user = gc.Garmin.get_full_name(client)
print(user)  
  
units = gc.Garmin.get_unit_system(client)
print(units)

sleepdata =  gc.Garmin.get_sleep_data(client,today.isoformat())
print(sleepdata)


act = gc.Garmin.get_activities(client,0,1)
print(act)