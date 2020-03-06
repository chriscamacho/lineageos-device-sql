#!/usr/bin/env python

# assuming python3

import sqlite3

db = sqlite3.connect('devices.sqlite')
cursor = db.cursor()

db.row_factory = sqlite3.Row
#cursor.execute('''select codename from devices where battery_removable='True' and channels="['nightly']"''')
cursor.execute('''select codename from devices where battery_removable='True' and channels like "%'nightly'%"''')
#cursor.execute('''select codename,versions from devices where versions like "%17%"  ''')
for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
    #print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))
    print('{0} '.format(row[0]), end="")

print()
db.close()
