


from garminconnect import Garmin as gc
import datetime
import pandas as pd
import os

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

#set todays date
today = datetime.date.today()

#create a garmin api session
client = gc(email,pwd)
gc.login(client)


#convert the json files to dataframes
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
                print(thedict[dfthedata.name])
                print(type(thedict[dfthedata.name]))
                thedict[dfthedata.name] = thedict[dfthedata.name].append(dfthedata)

                print(dfthedata.name)
                print(dfthedata)
            else:
                print('somthing wrong level 2 create_dataframe')
        else:
                print('somthing wrong level 1 create_dataframe')


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

def df_to_csv(data, fileName,date_stamp): #create csv file
   cwd = os.getcwd()#get the current working directory
   # Save all data files to a sub directory to aviod cultering
   csvname = cwd + '/data/'+ fileName+ '_' + str(date_stamp.strftime('%Y%m%d%H%M%S')) + '.csv'
   data.to_csv(csvname)


def unest(data, dictdata):

        if not bool(dictdata):
            dictdata = create_sleep_dataframe(data)
        elif bool(dictdata):  # if the dict is not empty then pass and append need data to the existing dataframes
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


dictdata = {}
for i in range(2, 3):

    iterdate = today - datetime.timedelta(days=i)

#break sleep data down into dataframes and export to CSV
    data = gc.get_sleep_data(client, iterdate.isoformat())
    dictdata = unest(data, dictdata)
#convert daily HR data to one CSV
    data = gc.get_heart_rates(client, iterdate.isoformat())
    df = pd.DataFrame(filterTheDict(data, (dict, list)),index=[0])
    df.name = 'Heart Rate Summary'
    
    
    
    dictdata[df.name] = dictdata[df.name].append(df)
    dictdata = unest(data, dictdata)
    df =  dictdata[df.name] = dictdata[df.name].append(df)
#convert daily stats and body compostion to one CSV
    data = gc.get_stats_and_body(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    df.name = 'stats + body comp'
    dictdata[df.name] = dictdata[df.name].append(df)
#convert daily step to one CSV
    #data = gc.get_steps_data(client, iterdate.isoformat())
    #df = pd.json_normalize(data)
    #df.name = 'steps data'
    #dictdata[df.name] = dictdata[df.name].append(df)



for k  in dictdata.keys():
       df_to_csv(dictdata[k], k,today)


