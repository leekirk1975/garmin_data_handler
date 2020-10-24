


from garminconnect import Garmin as gc
import datetime
import pandas as pd

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()


client = gc(email,pwd)
gc.login(client)


def create_dataframe(thedata):

    for i in thedata:

        thedatadf = convert_json_to_df(thedata[i])
        thedatadf.name = list(thedata.keys())[0]
        print(thedatadf.name)



def convert_json_to_df(thedata):

        if isinstance(thedata ,dict):
            thedatalist = list(thedata.items())
            # index = 0 to aviod "ValueError: If using all scalar values, you must pass an index"
            df = pd.DataFrame(thedata, index=[0]) #https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi

        elif isinstance(thedata, list):
            df = pd.DataFrame(thedata)
        else:
            print("type not list or dict")

        return df

#df = pd.DataFrame.from_dict(sleepdata)

for i in range(1,100):

    iterdate = today - datetime.timedelta(days=i)
    sleepdata =  gc.get_sleep_data(client,iterdate.isoformat())
    #print(sleepdata)
    create_dataframe(sleepdata)



#Write_Data_to_csv (df_activity_streams, 'Activity_streams',date_stamp)
#print('finished sleepdata '+' '+ str(iterdate)