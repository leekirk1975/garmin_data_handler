

import os
import garminexport
from fitparse import FitFile




cwd = os.getcwd()  # get the current working directory
# Save all data files to a sub directory to aviod cultering
file = cwd + '/data/5623904498.fit'
#file = cwd + '/data/2020-10-03/69156120772.fit'
print (file)
fitfile = FitFile(file)






# Get all data messages that are of type record
for record in fitfile.get_messages('record'):

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
