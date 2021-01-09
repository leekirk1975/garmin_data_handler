from fitparse import FitFile
import os

# Getting the current work directory (cwd)
cwd = os.getcwd()

# class fit_event_handler(object):
#
#
#     pass


for roots, dirs, files in os.walk(cwd):
    for file in files:
        if file.endswith(".fit"):
            print(os.path.join(roots, file))

# included messages
# file_id, event, sport, record, HRV, session
cwd = os.getcwd()  # get the current working directory
# Note The file name needs to be reformatted from to 2020-12-04T21:22:38+00:00_5913788595.fit'
file = cwd + '/data/garmin_backup/2020-12-04T21:22:38+00:00_5913788595.fit'
# '2020-12-04T21:22:38+00:00_5913788595.fit'
print(file)

fitfile = FitFile(file)

# Get all data messages that are of type record
# include:
# exclude: file_id,'file_creator','unknown','device_settings','user_profile','zones_target'
fit_record_type = ['event', 'sport','record','hrv']

for record_type in fit_record_type:
    for record in fitfile.get_messages(record_type):
        # Go through all the data entries in this record
        for record_data in record:

            # Print the records name and value (and units if it has any)

            if record_data.units and 'unknown' not in record_data.name:
                print(" * %s: %s %s" % (
                    record_data.name, record_data.value, record_data.units,
                ))
            elif 'unknown' not in record_data.name:
                print(" * %s: %s" % (record_data.name, record_data.value))
        print()
