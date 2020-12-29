from garminconnect import Garmin as GC
import datetime
import pandas as pd
import os

# import csv


# get login and password
email, pwd = open('GamrinDetails.txt').read().strip().split(',')

# set today's date
today = datetime.date.today()

# create a garmin api session
client = GC(email, pwd)
GC.login(client)


# Deal with the special case of sleepdata - convert json files to dataframes
def create_sleep_dataframe(thedata, thedict={}):
    for i in thedata:
        if isinstance(thedata[i],
                      (dict, list)):  # skip any field from the json file that is not data in a list or dictionary
            dfthedata = convert_json_to_df(thedata[i])  # convert the jason field to a DF
            dfthedata.name = i
            if dfthedata.name not in thedict.keys():
                # if this is the first data set create a new df name after the data set and add it to a dictonary
                thedict[dfthedata.name] = dfthedata
            elif dfthedata.name in thedict.keys():
                # append any additional data to the existing dataframe in the dict
                thedict[dfthedata.name] = thedict[dfthedata.name].append(dfthedata)
            else:
                pass
        else:
            pass

    return (thedict)


# handle the unesting of the sleep DF - unquie case.
def unest(data, dictdata):
    if not bool(dictdata):
        dictdata = create_sleep_dataframe(data)
    elif bool(dictdata):  # if the dict is not empty then pass and append data to the existing dataframes
        dictdata = create_sleep_dataframe(data, dictdata)
    return dictdata


# convert json and list to dataframes
def convert_json_to_df(thedatafield):
    if isinstance(thedatafield, dict):
        # index = 0 to aviod "ValueError: If using all scalar values, you must pass an index"
        df = pd.DataFrame(thedatafield, index=[
            0])
        # https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
    elif isinstance(thedatafield, list):
        df = pd.DataFrame(thedatafield)
    else:
        df = None
        print("type not list or dict")

    return df


# write from a dataframe to CSV
def df_to_csv(data, filename, date_stamp):  # create csv file
    cwd = os.getcwd()  # get the current working directory
    # Save all data files to a sub directory to aviod cultering
    csvname = cwd + '/data/' + filename + ' raw data.csv'  # + '_' + str(date_stamp.strftime('%Y%m%d%H%M%S')) + '.csv'
    data.to_csv(csvname, index=False)


# Iterate over all the key value pairs in dictionary and call the given callback function()
# on each pair. Items for which callback() returns True, add them to the new dictionary.
# In the end return the new dictionary.
def filterthedict(dictobj, callback):
    newdict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictobj.items():
        # Check if item satisfies the given condition then add to new dict
        if not isinstance(value, list):
            newdict[key] = value
    return newdict


# Create a new df if it does not exist and thereafter append any new data
def df_create_append(df, dictdata, name):
    df.name = name
    if df.name in dictdata.keys():
        dictdata[df.name] = dictdata[df.name].append(df)
    elif df.name not in dictdata.keys():
        dictdata[df.name] = df
    return dictdata


# convert a string to date format
def convert_date(format_str, date_str):
    return datetime.datetime.strptime(date_str, format_str).date()


# Get data from garmin
# set-up empty dict top store all the DF
dictdata = {}
start = 0
end = 0

# 1) check if the CSV file exists, if not load all the data.
# If the file exists then 1) open CSV file, 2) load the CSV file in a panadas data frame
# 3) append anynew data 4) save the updated csv file

# list of the CSV files to dump the garmin query data
lstfiles = ['stats_body_comp', 'daily_steps', 'Heart_Rate_details', 'Heart_Rate_Summary', 'sleepStress',
            'wellnessEpochRespirationDataDTOList', 'wellnessEpochSPO2DataDTOList', 'wellnessSpO2SleepSummaryDTO',
            'sleepLevels', 'sleepMovement', 'dailySleepDTO',
            'activities summaries']

for filename in lstfiles:
    cwd = os.getcwd()  # get the current working directory
    csv_file_name = cwd + '/data/' + filename + " raw data.csv"
    file_exists = os.path.isfile(csv_file_name)

    if file_exists:  # check to see if the files already exist, if they do then check the last data
        df_his_data = pd.read_csv(csv_file_name)
        # Get the start date once
        if filename == 'stats_body_comp':
            date_str = df_his_data['calendarDate'].iloc[-1]  # get the last date in the series
            last_date = convert_date('%Y-%m-%d', date_str)
            end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
            start = 0
            end = start + abs((last_date - end_date).days)  # fdetermine number of days of data to collect
            print("The last date in the file is " + last_date.strftime("%m/%d/%Y") + " #records to add " + str(end))

        print("file exists, now loading data from " + csv_file_name)
        # append df to dict
        dictdata = df_create_append(df_his_data, dictdata, filename)

    else:  # get the histroy between the start end day range
        print('files do not exist, writing new files')
        start = 1
        end = 400
        break  # exit for loop as it is not needed

# Get  garmin connect healthdata in the selected data range and create/append to CSV files
for i in range(end, start, -1):

    iterdate = today - datetime.timedelta(days=i)
    print(iterdate)
    # Deal with Garmin Json data break Json sleep data down into two dataframes
    # 1) sleep summary 2) sleep interday details and export to CSV
    data = GC.get_sleep_data(client, iterdate.isoformat())
    dictdata = unest(data, dictdata)
    # convert daily HR data to one CSV
    data = GC.get_heart_rates(client, iterdate.isoformat())
    # extract the daily heart rate summary data excluding any list create a  df
    df = pd.DataFrame(filterthedict(data, (dict, list)), index=[0])
    df.name = 'Heart_Rate_Summary'
    if df.name in dictdata.keys():
        dictdata[df.name] = dictdata[df.name].append(df)
    elif df.name not in dictdata.keys():
        dictdata[df.name] = df
    # extract the list with the detail heart rate data merge into one data frame
    df = pd.DataFrame(data['heartRateValues'], columns=['timestamp', 'heatRateValues'])
    dictdata = df_create_append(df, dictdata, 'Heart_Rate_details')
    # convert daily stats and body compostion to one CSV
    data = GC.get_stats_and_body(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dictdata = df_create_append(df, dictdata, 'stats_body_comp')
    # convert daily step to one CSV
    data = GC.get_steps_data(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dictdata = df_create_append(df, dictdata, 'daily_steps')

# this picks up the power curve and the Vo2 max
data = GC.get_activities(client, start, end)
df = pd.json_normalize(data)
dictdata = df_create_append(df, dictdata, 'activities summaries')

# loop through the dict of dataframes write a CSV file for each one
for k in dictdata.keys():
    df_to_csv(dictdata[k], k, today)
