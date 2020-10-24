


from garminexport import garminclient as gec
from datetime import date

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = date.today()

client1 = gec.GarminClient (email,pwd)
gec.GarminClient.connect(client1)
act_summary = gec.GarminClient.get_activity_summary(client1,'5670672729')
print(act_summary)

act_list = gec.GarminClient.list_activities(client1)
print (act_list)

act_details = gec.GarminClient.get_activity_details(client1,'5670672729')
print (act_details)