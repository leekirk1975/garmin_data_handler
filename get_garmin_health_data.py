
from garminconnect import Garmin as gc
import datetime
import pandas as pd
import os

#get login and password
email, pwd  = open('GamrinDetails.txt').read().strip().split(',')

#set todays date
today = datetime.date.today()

#create a garmin api session
client = gc(email,pwd)
gc.login(client)

'''
convert the json files to dataframes
'''
def create_sleep_dataframe(thedata, thedict ={}):

    for i in thedata:
        if isinstance(thedata[i], (dict,list)):#skip any field from the json file that is not data in a list or dictionary
            dfthedata = convert_json_to_df(thedata[i]) #convert the jason field to a DF
            dfthedata.name = i
            if dfthedata.name not in thedict.keys():
                #if this if the firt data set create a new df name after the data set and add it to a dictonary
                thedict[dfthedata.name] = dfthedata
            elif dfthedata.name in thedict.keys():
                #append additional data to the existing dataframe in the dict
                thedict[dfthedata.name] = thedict[dfthedata.name].append(dfthedata)
            else:
                print('skip level 2 create_dataframe')
        else:
                print('skip level 1 create_dataframe')

    return(thedict)


#convert json and list to dataframes
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

#write from data frame to CSV
def df_to_csv(data, fileName,date_stamp): #create csv file
   cwd = os.getcwd()#get the current working directory
   # Save all data files to a sub directory to aviod cultering
   csvname = cwd + '/data/'+ fileName+ '_' + str(date_stamp.strftime('%Y%m%d%H%M%S')) + '.csv'
   data.to_csv(csvname)

#handle the unesting of the sleep DF - unquie case.
def unest(data, dictdata):
        if not bool(dictdata):
            dictdata = create_sleep_dataframe(data)
        elif bool(dictdata):  # if the dict is not empty then pass and append data to the existing dataframes
            dictdata = create_sleep_dataframe(data, dictdata)
        return dictdata

'''
Iterate over all the key value pairs in dictionary and call the given
callback function() on each pair. Items for which callback() returns True,
add them to the new dictionary. In the end return the new dictionary.
'''
def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if not isinstance(value, list):
            newDict[key] = value
    return newDict
'''
handle creation of the df if it does not exist and thereafter  append new data
'''
def df_create_append(df, dictdata, name):
    df.name = name
    if df.name in dictdata.keys():
        dictdata[df.name] = dictdata[df.name].append(df)
    elif df.name not in dictdata.keys():
        dictdata[df.name] = df
    return dictdata

dictdata = {}

#Get all garmin connect health data and exprt to CSV files
#loop from today-2 until x days to collect history
for i in range(2, 700):

    iterdate = today - datetime.timedelta(days=i)

#Deal with Garmin Json data break Json sleep data down into two dataframes 1) sleep summary 2) sleep interday details and export to CSV
    data = gc.get_sleep_data(client, iterdate.isoformat())
    dictdata = unest(data, dictdata)
#convert daily HR data to one CSV
    data = gc.get_heart_rates(client, iterdate.isoformat())
    #extract the daily heart rate summary data excluding any list create a  df
    df = pd.DataFrame(filterTheDict(data, (dict, list)),index=[0])
    df.name = 'Heart_Rate_Summary'
    if df.name in dictdata.keys():
        dictdata[df.name] = dictdata[df.name].append(df)
    elif df.name not in dictdata.keys():
        dictdata[df.name] = df
    #extract the list with the detail heart rate data merge into one data frame
    df = pd.DataFrame(data['heartRateValues'],columns=['timestamp','heatRateValues'])
    dictdata = df_create_append(df,dictdata,'Heart_Rate_details')
#convert daily stats and body compostion to one CSV
    data = gc.get_stats_and_body(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dictdata = df_create_append(df,dictdata,'stats_body_comp')
    #convert daily step to one CSV
    data = gc.get_steps_data(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dictdata = df_create_append(df,dictdata,'daily_steps')

#this picks up the power curve and the Vo2 max
data  = gc.get_activities(client,0,700)
df = pd.json_normalize(data)

dictdata = df_create_append(df,dictdata,'activities summaries')

#loop through the dict of dataframes write a CSV file for each one
for k  in dictdata.keys():
    df_to_csv(dictdata[k], k,today)


