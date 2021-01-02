import datetime
import dateutil
import pandas as pd
import get_garmin_health_data as ggh
import os

# set today's date
today = datetime.date.today()
cwd = os.getcwd()  # get the current working directory
# list of the CSV files to dump the garmin query data
lst_files = ['stats_body_comp', 'daily_steps', 'Heart_Rate_details', 'Heart_Rate_Summary', 'sleepStress',
             'wellnessEpochRespirationDataDTOList', 'wellnessEpochSPO2DataDTOList', 'wellnessSpO2SleepSummaryDTO',
             'sleepLevels', 'sleepMovement', 'dailySleepDTO',
             'activities summaries']

# lst of list of redundant series to drop form each data set
dict_drop_list = {"stats_body_comp": ['consumedKilocalories', 'wellnessDescription', 'includesWellnessData',
                                      'privacyProtected', 'lastSyncTimestampGMT', 'userDailySummaryId', 'uuid',
                                      'rule.typeId', 'rule.typeKey', 'from', 'until'],
                  "daily_steps": [],
                  "Heart_Rate_details": [],
                  "Heart_Rate_Summary": [],
                  "sleepStress": [],
                  "wellnessEpochRespirationDataDTOList": [],
                  "wellnessEpochSPO2DataDTOList": ['deviceId'],
                  "wellnessSpO2SleepSummaryDTO": ['deviceId', 'alertThresholdValue', 'numberOfEventsBelowThreshold',
                                                  'durationOfEventsBelowThreshold'],
                  "sleepLevels": [],
                  "sleepMovement": [],
                  "dailySleepDTO": ['autoSleepStartTimestampGMT', 'autoSleepEndTimestampGMT', 'retro',
                                    'sleepQualityTypePK', 'sleepResultTypePK', 'spo2Threshold'],
                  "activities summaries": ['averageSwimCadenceInStrokesPerMinute', 'maxSwimCadenceInStrokesPerMinute',
                                           'averageSwolf', 'activeLengths',
                                           'steps', 'conversationUuid', 'conversationPk', 'numberOfActivityLikes',
                                           'numberOfActivityComments',
                                            'likedByUser', 'commentedByUser', 'activityLikeDisplayNames',
                                           'activityLikeFullNames','requestorRelationship',
                                            'userRoles', 'userPro', 'courseId', 'poolLength', 'unitOfPoolLength',
                                           'hasVideo', 'videoUrl', 'deviceId',
                                           'workoutId', 'avgStrokes', 'minStrokes', 'avgDoubleCadence',
                                           'maxDoubleCadence', 'summarizedExerciseSets',
                                           'maxDepth', 'avgDepth', 'surfaceInterval', 'startN2', 'endN2', 'startCns',
                                           'endCns', 'activityLikeAuthors', 'diveNumber',
                                           'bottomTime', 'minAirSpeed', 'maxAirSpeed', 'avgAirSpeed', 'avgWindYawAngle',
                                           'minCda', 'maxCda', 'avgCda', 'avgWattsPerCda',
                                           'flow', 'grit', 'jumpCount', 'totalSets', 'activeSets', 'totalReps',
                                           'avgFlow', 'avgGrit', 'favorite', 'decoDive', 'autoCalcCalories',
                                           'parent', 'purposeful', 'atpActivity', 'elevationCorrected',
                                           'summarizedDiveInfo.weightUnit', 'summarizedDiveInfo.visibility',
                                           'summarizedDiveInfo.visibilityUnit', 'summarizedDiveInfo.surfaceCondition',
                                           'summarizedDiveInfo.current', 'summarizedDiveInfo.waterType',
                                           'summarizedDiveInfo.waterDensity', 'summarizedDiveInfo.summarizedDiveGases',
                                           'summarizedDiveInfo.totalSurfaceTime']}
df_dict = {}

for filename in lst_files:

    csv_filename = cwd + '/data/' + filename + " raw data.csv"
    file_exists = os.path.isfile(csv_filename)

    if file_exists:  # check to see if the files already exist, if they do then check the last data
        print("{} exists starting cleaning data".format(filename))
        df_raw_data = pd.read_csv(csv_filename)
        df_raw_data.name = filename

        # clean series
        # go through each file, dropping any series that is not going to be used.
        if dict_drop_list[filename]:  # if the list is not empty then
            [df_raw_data.drop(drop_series, axis=1, inplace=True) for drop_series in dict_drop_list[filename]]

        # append all DF to a single dictionary
        df_dict = ggh.df_create_append(df_raw_data, df_dict, df_raw_data.name)

    else:  # get the history between the start end day range
        print("{} does not exist exiting ".format(filename))

# loop through the dict of dataframes write a CSV file for each one
for df_item in df_dict.keys():
    ggh.df_to_csv(df_dict[df_item], df_item, ' clean data.csv', today)
