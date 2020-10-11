

import garminexport
import garminconnect as gc

email, pwd  = open('GamrinDetails.txt').read().strip().split(',')#set the client secret and refresh token

client = gc.Garmin(email,pwd)


print(gc.Garmin.get_full_name(client))
