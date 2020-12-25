

import os
from fitparse import FitFile


import os

# Getting the current work directory (cwd)
thisdir = os.getcwd()

# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".fit"):
            print(os.path.join(r, file))

cwd = os.getcwd()  # get the current working directory
file = cwd + '/data/garmin_backup/2020-11-22T09:11:21+00:00_5856698684.fit'
                                #'2020-11-22T09:11:21+00:00_5856698684.fit'
print (file)

fitfile = FitFile(file)

# Get all data messages that are of type record
for record in fitfile.get_messages('event'):

    # Go through all the data entries in this record
    for record_data in record:

        # Print the records name and value (and units if it has any)
        if record_data.units:
            print(" * %s: %s %s" % (
                record_data.name, record_data.value, record_data.units,
            ))
        else:
            print(" * %s: %s" % (record_data.name, record_data.value))
    print()