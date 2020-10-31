


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
            dictdata = create_dataframe(data)
        elif bool(dictdata):  # if the dict is not empty then pass and append need data to the existing dataframes
            dictdata = create_dataframe(data, dictdata)
        return dictdata



#SLEEP DATA
#iterate through the historical garmin sleep data series, convert json data to dataframes
# and then output a csvfile for each data frame
#dictsleep={}
# for i in range(2,3):
#
#     iterdate = today - datetime.timedelta(days=i)
#
#     sleepdata =  gc.get_sleep_data(client,iterdate.isoformat())
#     if not bool(dictsleep):
#         dictsleep = create_dataframe(sleepdata)
#     elif bool(dictsleep): #if the dict is not empty then pass and append need data to the existing dataframes
#         dictsleep = create_dataframe(sleepdata,dictsleep)
#
# for i  in dictsleep.keys():
#       df_to_csv(dictsleep[i], i,today)

# Get body comp and user stats
# iterate through the historical garmin sleep data series, convert json data to dataframes
# and then output a csvfile for each data frame
dictdata = {}
for i in range(2, 3):

    iterdate = today - datetime.timedelta(days=i)

    data = gc.get_sleep_data(client, iterdate.isoformat())
    dictdata = unest(data, dictdata)
    data = gc.get_heart_rates(client, iterdate.isoformat())
    dictdata = unest(data, dictdata)
    data = gc.get_steps_data(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    #df.name = data
    #dictdata[data.name] = dictdata[data.name].append(dfthedata)
    #data = gc.get_stats_and_body(client, iterdate.isoformat())



for k  in dictdata.keys():
       df_to_csv(dictdata[k], k,today)


