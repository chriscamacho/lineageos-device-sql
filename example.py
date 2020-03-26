#!/usr/bin/env python

# assuming python3

import sqlite3

db = sqlite3.connect('devices.sqlite')
cursor = db.cursor()

db.row_factory = sqlite3.Row
#cursor.execute('''select codename from devices where battery_removable='True' and channels like "%'nightly'%"''')
#cursor.execute('''select codename,versions from devices where channels like "%'nightly'%"''')
cursor.execute('''select name,sdcard,cpu,cpu_cores,cpu_freq,gpu,codename from devices where versions like "%17%" and battery_removable='True' ''')
for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
    #print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))
    print('{6} {0} sdcard:{1}  cpu:{2} cores: {3}cores @{4} {5}'.format(
    row[0],row[1],row[2],row[3],row[4],row[5],row[6]), end="\n")

print()
db.close()
