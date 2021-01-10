from fitparse import FitFile
import pandas as pd
import datetime
import os
import get_garmin_health_data as ggh


# included messages
# file_id, event, sport, record, HRV, session
cwd = os.getcwd()  # get the current working directory
# Note The file name needs to be reformatted from to 2020-12-04T21:22:38+00:00_5913788595.fit'
file = cwd + '/data/garmin_backup/2020-12-04T21:22:38+00:00_5913788595.fit'
# '2020-12-04T21:22:38+00:00_5913788595.fit'

fitfile = FitFile(file)

# Get all data messages that are of type record
# include:
# exclude: file_id,'file_creator','unknown','device_settings','user_profile','zones_target'
fit_record_type = ['record', 'hrv' ,'event'] #, 'sport']
workout_id = file[-14:-4]
dict_df_workouts = {}

for record_type in fit_record_type:
    list_workouts = []
    list_labels = ['start', 'end']

    for record in fitfile.get_messages(record_type):
        # Go through all the data entries in this record
        workout_dict = {}
        for record_data in record:

            # # Print the records name and value (and units if it has any)
            # if record_data.units and 'unknown' not in record_data.name:
            #     print(" * %s: %s %s" % (
            #         record_data.name, record_data.value, record_data.units))
            #
            #     if isinstance(record_data.value, (list,tuple)):
            #
            #         for item, label  in zip(record_data.value, list_labels):
            #             workout_dict[record_data.name + '_' + label] = item
            #     else:
            #         workout_dict[record_data.name] = record_data.value

            if 'unknown' not in record_data.name:
                # print(" * %s: %s" % (record_data.name, record_data.value))

                if isinstance(record_data.value, (list, tuple)) and record_type == record:
                    for item, label in zip(record_data.value, list_labels):
                        workout_dict[record_data.name + '_' + label] = item
                else:
                    workout_dict[record_data.name] = record_data.value

        workout_dict['workout ID'] = workout_id
        list_workouts.append(workout_dict)
        # print()

    df_workouts = pd.DataFrame(list_workouts)
    df_workouts.name = record_type
    dict_df_workouts = ggh.df_create_append(df_workouts, dict_df_workouts, record_type)
print(dict_df_workouts)

# Save all data files to a sub directory to avoid cluttering
for df_item in dict_df_workouts.keys():
    name = workout_id + ' ' + df_item + ' raw data.csv'
    ggh.df_to_csv(dict_df_workouts[df_item], df_item, name)
