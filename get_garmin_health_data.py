


from garminconnect import Garmin as gc
import datetime

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()


client = gc(email,pwd)
gc.login(client)

for i in range(0,30):

    startdate = today - datetime.timedelta(days=i)
    sleepdata =  gc.get_sleep_data(client,startdate.isoformat())
    print(sleepdata)