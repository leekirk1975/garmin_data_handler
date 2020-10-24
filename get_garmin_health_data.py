


from garminconnect import Garmin as gc
import datetime
import pandas as pd

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()


client = gc(email,pwd)
gc.login(client)


def create_dataframe(thedata, thedict = None):

    dictdf = {}

    for i in thedata:
        if isinstance(thedata[i], (dict,list)):#skip any field from the json file that is not data in a list or dictionary
            dfthedata = convert_json_to_df(thedata[i]) #convert the jason field to a DF
            dfthedata.name = i
            if thedict is None:
                dictdf[dfthedata.name] = dfthedata
            elif dfthedata.name  in thedict.keys():

                print(dfthedata.name)
                print(dfthedata)
            else:
                print('somthing wrong')



    return(dictdf)


def convert_json_to_df(thedatafield):

        if isinstance(thedatafield ,dict):
            # index = 0 to aviod "ValueError: If using all scalar values, you must pass an index"
            df = pd.DataFrame(thedatafield, index=[0]) #https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        elif isinstance(thedatafield, list):
            df = pd.DataFrame(thedatafield)
        else:
            df = None
            print("type not list or dict")

        return df

#def df_to_csv()
    #Write_Data_to_csv (df_activity_streams, 'Activity_streams',date_stamp)
    #print('finished sleepdata '+' '+ str(iterdate)
    
dictsleep={}
#iterate through the historical data series
for i in range(2,4):

    iterdate = today - datetime.timedelta(days=i)
    
    sleepdata =  gc.get_sleep_data(client,iterdate.isoformat())
    #print(sleepdata)
    if not bool(dictsleep):
        dictsleep = create_dataframe(sleepdata)
    elif bool(dictsleep): #if the dict is not empty then pass and append need data to the existing dataframes
        dictsleep = create_dataframe(sleepdata,dictsleep )


