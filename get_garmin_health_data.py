from garminconnect import Garmin as GC
import datetime
import pandas as pd
import os
import utilities as util


# get login and password
email, pwd = open('GarminDetails.txt').read().strip().split(',')

# set today's date
today = datetime.date.today()
cwd = os.getcwd()  # get the current working directory

# create a garmin api session
client = GC(email, pwd)
GC.login(client)


# Deal with the special case of sleepdata - convert json files to dataframes
def create_sleep_dataframe(thedata, thedict=None):
    if thedict is None:
        thedict = {}
    for sleepitem in thedata:
        if isinstance(thedata[sleepitem],
                      (dict, list)):  # skip any field from the json file that is not data in a list or dictionary
            dfthedata = convert_json_to_df(thedata[sleepitem])  # convert the jason field to a DF
            dfthedata.name = sleepitem
            if dfthedata.name not in thedict.keys():
                # if this is the first data set create a new df name after the data set and add it to a dictionary
                thedict[dfthedata.name] = dfthedata
            elif dfthedata.name in thedict.keys():
                # append any additional data to the existing dataframe in the dict
                thedict[dfthedata.name] = thedict[dfthedata.name].append(dfthedata)
            else:
                pass
        else:
            pass

    return thedict


# handle the unesting of the sleep DF - unique case.
def unest(unest_data, unest_dict_data):
    if not bool(unest_dict_data):
        unest_dict_data = create_sleep_dataframe(unest_data)
    elif bool(unest_dict_data):  # if the dict is not empty then pass and append data to the existing dataframes
        unest_dict_data = create_sleep_dataframe(unest_data, unest_dict_data)
    return unest_dict_data


# convert json and list to dataframes
def convert_json_to_df(thedatafield):
    if isinstance(thedatafield, dict):
        # index = 0 to aviod "ValueError: If using all scalar values, you must pass an index"
        df1 = pd.DataFrame(thedatafield, index=[
            0])
        # https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
    elif isinstance(thedatafield, list):
        df1 = pd.DataFrame(thedatafield)
    else:
        df1 = None
        print("type not list or dict")

    return df1


# Iterate over all the key value pairs in dictionary and call the given callback function()
# on each pair. Items for which callback() returns True, add them to the new dictionary.
# In the end return the new dictionary.
def filterthedict(dictobj):
    newdict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictobj.items():
        # Check if item satisfies the given condition then add to new dict
        if not isinstance(value, list):
            newdict[key] = value
    return newdict


# # Create a new df if it does not exist and thereafter append any new data
# def df_create_append(df2, dict_data_append, name):
#     df2.name = name
#     if df2.name in dict_data_append.keys():
#         dict_data_append[df2.name] = dict_data_append[df2.name].append(df2)
#     elif df2.name not in dict_data_append.keys():
#         dict_data_append[df2.name] = df2
#     return dict_data_append


# convert a string to date format
def convert_date(format_str, date_str):
    return datetime.datetime.strptime(date_str, format_str).date()


# Get data from garmin
# set-up empty dict top store all the DF
dict_data = {}
start = 0
end = 0

# 1) check if the CSV file exists, if not load all the data.
# If the file exists then 1) open CSV file, 2) load the CSV file in a pandas data frame
# 3) append anynew data 4) save the updated csv file

# list of the CSV files to dump the garmin query data
lstfiles = ['stats_body_comp', 'daily_steps', 'Heart_Rate_details', 'Heart_Rate_Summary', 'sleepStress',
            'wellnessEpochRespirationDataDTOList', 'wellnessEpochSPO2DataDTOList', 'wellnessSpO2SleepSummaryDTO',
            'sleepLevels', 'sleepMovement', 'dailySleepDTO',
            'activities summaries']

for filename in lstfiles:
    csv_file_name = cwd + '/data/' + filename + " raw data.csv"
    file_exists = os.path.isfile(csv_file_name)

    if file_exists:  # check to see if the files already exist, if they do then check the last data
        df_his_data = pd.read_csv(csv_file_name)
        # Get the start date once
        if filename == 'stats_body_comp':
            this_date_str = df_his_data['calendarDate'].iloc[-1]  # get the last date in the series
            last_date = convert_date('%Y-%m-%d', this_date_str)
            end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
            start = 0
            end = start + abs((last_date - end_date).days)  # fdetermine number of days of data to collect
            print("The last date in the file is " + last_date.strftime("%m/%d/%Y") + " #records to add " + str(end))

        print("file exists, now loading data from " + csv_file_name)
        # append df to dict
        dict_data = util.df_create_append(df_his_data, dict_data, filename)

    else:  # get the history between the start end day range
        print('files do not exist, writing new files')
        start = 1
        end = 450
        break  # exit for loop as it is not needed

# Get  garmin connect healthdata in the selected data range and create/append to CSV files
for i in range(end, start, -1):

    iterdate = today - datetime.timedelta(days=i)
    print(iterdate)
    # Deal with Garmin Json data break Json sleep data down into two dataframes
    # 1) sleep summary 2) sleep interday details and export to CSV
    data = GC.get_sleep_data(client, iterdate.isoformat())
    dict_data = unest(data, dict_data)
    # convert daily HR data to one CSV
    data = GC.get_heart_rates(client, iterdate.isoformat())
    # extract the daily heart rate summary data excluding any list create a  df
    df = pd.DataFrame(filterthedict(data), index=[0])
    df.name = 'Heart_Rate_Summary'
    if df.name in dict_data.keys():
        dict_data[df.name] = dict_data[df.name].append(df)
    elif df.name not in dict_data.keys():
        dict_data[df.name] = df
    # extract the list with the detail heart rate data merge into one data frame
    df = pd.DataFrame(data['heartRateValues'], columns=['timestamp', 'heatRateValues'])
    dict_data = util.df_create_append(df, dict_data, 'Heart_Rate_details')
    # convert daily stats and body composition to one CSV
    data = GC.get_stats_and_body(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dict_data = util.df_create_append(df, dict_data, 'stats_body_comp')
    # convert daily step to one CSV
    data = GC.get_steps_data(client, iterdate.isoformat())
    df = pd.json_normalize(data)
    dict_data = util.df_create_append(df, dict_data, 'daily_steps')

# this picks up the power curve and the Vo2 max
data = GC.get_activities(client, start, end)
df = pd.json_normalize(data)
dict_data = util.df_create_append(df, dict_data, 'activities summaries')

# loop through the dict of dataframes write a CSV file for each one
for k in dict_data.keys():
    util.df_to_csv(cwd, dict_data[k], k, ' raw data.csv')
