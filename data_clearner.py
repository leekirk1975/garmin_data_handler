import datetime
import dateutil
import pandas as pd
import os

cwd = os.getcwd()  # get the current working directory
# list of the CSV files to dump the garmin query data
lst_files = ['stats_body_comp', 'daily_steps', 'Heart_Rate_details', 'Heart_Rate_Summary', 'sleepStress',
             'wellnessEpochRespirationDataDTOList', 'wellnessEpochSPO2DataDTOList', 'wellnessSpO2SleepSummaryDTO',
             'sleepLevels', 'sleepMovement', 'dailySleepDTO',
             'activities summaries']

# lst of list of redundant series to drop form each data set
dict_drop_list = {"stats_body_comp": ['consumedKilocalories', 'wellnessDescription', 'includesWellnessData',
                                      'privacyProtected', 'lastSyncTimestampGMT', 'userDailySummaryId'],
                  "daily_steps": [],
                  "Heart_Rate_details": [],
                  "Heart_Rate_Summary": [],
                  "sleepStress": [],
                  "wellnessEpochRespirationDataDTOList": [],
                  "wellnessEpochSPO2DataDTOList": [],
                  "wellnessSpO2SleepSummaryDTO": [],
                  "sleepLevels": [], "sleepMovement": [],
                  "dailySleepDTO": [],
                  "activities summaries": []}

for filename in lst_files:

    csv_filename = cwd + '/data/' + filename + " raw data.csv"
    file_exists = os.path.isfile(csv_filename)

    if file_exists:  # check to see if the files already exist, if they do then check the last data
        print("{} exists starting cleaning data".format(filename))
        df_raw_data = pd.read_csv(csv_filename)

        # series clean
        # go through each file, dropping any series that is not going to be used.

        if dict_drop_list[filename]:  # if the list is not empty then
            [df_raw_data.drop(drop_series, axis=1, inplace=True) for drop_series in dict_drop_list[filename]]

    else:  # get the history between the start end day range
        print("{} does not exist exiting ".format(filename))
