from fitparse import FitFile
from fitparse import DataMessage
import pandas as pd
# import datetime
import os
import utilities as util

# dict to store all dataframes for export to csv
dict_df_workouts = {}

# Create list of all files with a .fit extension
cwd = os.getcwd()  # get the current working directory
#directory = cwd + '/data/garmin_backup/test/'
directory = cwd + '/data/garmin_backup/'
file_list = [filename for filename in os.listdir(directory) if filename.endswith(".fit")]

# process all the fit files in the list
for filename in file_list:
    this_file = directory + filename
    fit_file = FitFile(this_file)

    # include: record, hrv, event messages from the passed fit files
    # exclude: file_id,'file_creator','unknown','device_settings','user_profile','zones_target','sport'
    fit_record_type = ['record', 'hrv', 'event']  #
    # extract the workout ID from the fit file name
    workout_id = filename[-14:-4]
    print(workout_id)


    # get the sport of the current activity from the fit file
    this_sport = None
    for sport in fit_file.get_messages('sport'):
        this_sport = DataMessage.get_value(sport, 'sport')

    # only process fit files with cycling data (indoor or outdoor)
    if this_sport == 'cycling':

        for record_type in fit_record_type:
            list_workouts = []
            list_labels = ['start', 'end']

            for record in fit_file.get_messages(record_type):
                # Go through all the data entries in this record
                workout_dict = {}
                for record_data in record:

                    if 'unknown' not in record_data.name:  # exclude in field labelled unknown
                        #print(" * %s: %s" % (record_data.name, record_data.value))  # split power phase start and end records into two fields
                        if isinstance(record_data.value, (list, tuple)) and record_type == 'record':
                            for item, label in zip(record_data.value, list_labels):
                                workout_dict[record_data.name + '_' + label] = item
                        else:
                            workout_dict[record_data.name] = record_data.value

                workout_dict['workout ID'] = workout_id
                list_workouts.append(workout_dict)
                # print()

            df_workouts = pd.DataFrame(list_workouts)
            df_workouts.name = record_type
            dict_df_workouts = util.df_create_append(df_workouts, dict_df_workouts, record_type)
print(dict_df_workouts)

# Save all data to csv files
for df_item in dict_df_workouts.keys():
    util.df_to_csv(cwd + '/data/', dict_df_workouts[df_item], df_item, ' raw data.csv')
