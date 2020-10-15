


from garminexport import garminclient as gec
from datetime import date



email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = date.today()

client1 = gec.GarminClient (email,pwd)
gec.GarminClient.connect(client1)
act_test = gec.GarminClient.get_activity_summary(client1,'5670672729')
print(act_test)