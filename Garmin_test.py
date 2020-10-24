


from garminconnect import Garmin as gc
import datetime

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token



#set todays date
today = datetime.date.today()
startdate = today - datetime.timedelta(days=10)
MODERN_URL = 'https://connect.garmin.com/modern'


class Garmin_ext(gc):

    pass
    #https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailyStress/2020-03-05'
    url_body_stressDetails = MODERN_URL + '/proxy/wellness-service/wellness/dailyStress/'
    url_sleepdata = MODERN_URL + '/proxy/wellness-service/wellness/dailySleepData/'

    def get_dailyStress(self, cdate):  # cDate = 'YYYY-mm-dd'
        """
        Fetch available body composition data (only for cDate)
        """
        dailyStressurl = self.url_body_stressDetails + self.display_name + '?date=' + cdate
        self.logger.debug("Fetching daily stress  with url %s", dailyStressurl)

        return self.fetch_data(dailyStressurl)



client = gc(email,pwd)
gc.login(client)

client1 = Garmin_ext(email,pwd)
Garmin_ext.login(client1)

sleepdata =  gc.get_sleep_data(client,today.isoformat())
print(sleepdata)


#stress_data =  Garmin_ext.get_dailyStress(client1,today.isoformat())
#print(stress_data)

user = gc.get_full_name(client)
print(user)  
  
units = gc.get_unit_system(client)
print(units)

act_data =  gc.get_stats(client,today.isoformat())
print(act_data)

body_composition =  gc.get_body_composition(client,today.isoformat())
print(body_composition)

stats_and_body =  gc.get_stats_and_body(client,today.isoformat())
print(stats_and_body)

heart_rates =  gc.get_heart_rates(client,today.isoformat())
print(heart_rates)

act = gc.get_activities(client,0,1)
print(act)

activity_id = '5670672729'

#zip_data = gc.download_activity(client,activity_id,client.ActivityDownloadFormat.ORIGINAL)
#output_file = f"./{str(activity_id)}.zip"
#with open(output_file, "wb") as fb:
#    fb.write(zip_data)


