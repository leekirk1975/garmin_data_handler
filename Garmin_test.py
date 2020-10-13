

from garminexport import garminclient as gec
from garminconnect import Garmin as gc
from datetime import date

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

client1 = gec.GarminClient (email,pwd)
gec.GarminClient.connect(client1)
act_test = gec.GarminClient.get_activity_summary(client1,'5670672729')
print(act_test)

#set todays date
today = date.today()

client = gc(email,pwd)
gc.login(client)

user = gc.get_full_name(client)
print(user)  
  
units = gc.get_unit_system(client)
print(units)

sleepdata =  gc.get_sleep_data(client,today.isoformat())
print(sleepdata)

act_data =  gc.get_stats(client,today.isoformat())
print(act_data)

body_composition =  gc.get_body_composition(client,today.isoformat())
print(body_composition)

stats_and_body =  gc.get_stats_and_body(client,today.isoformat())
print(stats_and_body)

act = gc.get_activities(client,0,1)
print(act)

activity_id = '5670672729'

#zip_data = gc.download_activity(client,activity_id,client.ActivityDownloadFormat.ORIGINAL)
#output_file = f"./{str(activity_id)}.zip"
#with open(output_file, "wb") as fb:
#    fb.write(zip_data)

print('finished')