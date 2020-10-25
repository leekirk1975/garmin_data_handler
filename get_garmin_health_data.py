


from garminconnect import Garmin as gc
import datetime
import pandas as pd

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()


client = gc(email,pwd)
gc.login(client)


def create_dataframe(thedata, thedict ={}):


    for i in thedata:
        if isinstance(thedata[i], (dict,list)):#skip any field from the json file that is not data in a list or dictionary
            dfthedata = convert_json_to_df(thedata[i]) #convert the jason field to a DF
            dfthedata.name = i
            if dfthedata.name not in thedict.keys():
                #if this if the firt data set create a new df name after the data set and add it to a dictonary
                thedict[dfthedata.name] = dfthedata
            elif dfthedata.name in thedict.keys():
                #append additional data to the existing dataframe in the dict
                print(thedict[dfthedata.name])
                thedict[dfthedata.name].append(dfthedata)

                print(dfthedata.name)
                print(dfthedata)
            else:
                print('somthing wrong')



    return(thedict)


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
for i in range(2,6):

    iterdate = today - datetime.timedelta(days=i)
    
    sleepdata =  gc.get_sleep_data(client,iterdate.isoformat())
    #print(sleepdata)
    if not bool(dictsleep):
        dictsleep = create_dataframe(sleepdata)
    elif bool(dictsleep): #if the dict is not empty then pass and append need data to the existing dataframes
        dictsleep = create_dataframe(sleepdata,dictsleep)

print(dictsleep.keys())
print(dictsleep)
