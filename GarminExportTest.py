

import json
import pandas as pd
from pandas import json_normalize
from garminexport import garminclient as gec
from garminconnect import Garmin as gc
import datetime

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()

#client1 = gec.GarminClient (email,pwd)
#gec.GarminClient.connect(client1)



def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out



client = gc(email,pwd)
gc.login(client)

iterdate = today - datetime.timedelta(days=3)

thedict ={}

data =  gc.get_heart_rates(client,iterdate.isoformat())

df1 = pd.json_normalize(data)
for i in data:
    print(any(isinstance(i, dict) for i in data.values()))
    flat = flatten_json(data)
    df = pd.DataFrame(flat,index=[0])
    df.name = i
    thedict[df.name] = df
#df = pd.json_normalize(flat)

print(df)





#act_summary = gec.GarminClient.get_activity_summary(client1,'5670672729')
#print(act_summary)
#print(act_summary.keys())
#data = json_normalize(act_summary)
#print(data)
#flat = flatten_json(act_summary)
#df = pd.json_normalize(flat)

#print(df)


#act_list = #gec.GarminClient.list_activities(client1)
#print (act_list)

#breakpoint()

#act_details = #gec.GarminClient.get_activity_details(client1,'5670672729')
#print (act_details)