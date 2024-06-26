#!/usr/bin/env python

### TODO this is a hairy arsed hack!

import yaml
import os
import sqlite3
import re
import sys

def deviceNumFields(fileName):
    with open(fileName, 'r') as stream:
        try:
            dev = yaml.load(stream, Loader=yaml.FullLoader)
            return len(dev)
        except yaml.YAMLError as exc:
            return -1

def deviceFromYML(fileName):
    with open(fileName, 'r') as stream:
        try:
            dev = yaml.load(stream, Loader=yaml.FullLoader)
            return dev
        except yaml.YAMLError as exc:
            return exc


def deviceToSqlInsert(fileName):
    fieldname = 'network'
    sql = 'insert into devices ('
    dev = deviceFromYML(fileName)
    #print(dir(dev))
    fields={}
    for attr, value in dev.items():
        #print(attr, value)
        fieldProcessed = False

        if attr=='battery':
            for bat, bvl in enumerate(value):
                #print(value)
                #print (str(bat)+'  '+str(bvl)+' '+str(value[bat]))
                if bvl=='removable':
                    fields['battery_removable']=value[bvl]
                if bvl=='capacity':
                    fields['battery_capacity']=value[bvl]
                if bvl=='tech':
                    fields['battery_tech']=value[bvl]
            fieldProcessed = True

        if attr=='bluetooth':
            for bat, bvl in value.items():
                #print(bat+'  '+str(bvl))
                if bat=='spec':
                    fields['bt_spec'] = bvl
                if bat=='profiles':
                    fields['bt_profiles'] = bvl
            fieldProcessed = True

        if attr=='cameras':
            for cam, cvl in enumerate(value):
                #print(str(cam)+'  '+str(cvl))
                fieldname = 'cam'+str(cam)
                # probably ignore > cam1
                for cfv in cvl:
                    # python ya gotta love it!
                    fields[fieldname+cfv]=cvl[cfv]
                    #print(fieldname+cfv+'='+cvl[cfv])
            fieldProcessed = True

        if attr=='network':
            if value!=None:
                for net, nvl in enumerate(value):
                    #print (str(net)+"  "+str(nvl))
                    for nfv in nvl:
                        for n in nvl:
                            #print(n)
                            #print(nvl[n])
                            if n=='tech':
                                fieldname='network'+nvl[n]
                            if n=='bands':
                                #print(fieldname+'='+nvl[n])
                                fields[fieldname]=nvl[n]
                    # use network2G, network3G and network4G
                    fieldProcessed = True

        if attr=='dimensions':
            continue
        if attr=='screen':
            continue
        if attr=='quirks':
            continue

        if not fieldProcessed:
            fields[attr]=value

    # should now have all fields in fields dict...
    isFirst=True
    for fn, val in fields.items():
        #print(str(fn)+' = '+str(val))
        if not isFirst:
            sql+=', '
        isFirst = False
        sql+=str(fn)

    sql+=') VALUES ('

    isFirst=True
    for fn, val in fields.items():
        if not isFirst:
            sql+=', '
        isFirst = False
        val = re.sub('"', "'", str(val))
        sql+='"'+val+'"'

    sql+=');'
    return sql




devs=os.listdir('devices')

"""  testing
maxFields = -1
maxDevice = ''
for dev in devs:
    if dev.endswith('.yml'):
        f = deviceNumFields('devices/' + dev)
        if maxFields < f:
            maxFields = f
            maxDevice = dev
print('max fields =' + str(maxFields))
print('device :' + maxDevice)
"""

db = sqlite3.connect('devices.sqlite')
cursor = db.cursor()
cursor.execute('drop table if exists devices;')

"""
    TODO iterate all devices to find all the field names
"""

cursor.execute('''
create table devices(
architecture text,
battery_removable text,
battery_capacity text,
battery_tech text,
bt_spec text,
bt_profiles text,
cam0flash text,
cam0info text,
cam1flash text,
cam1info text,
cam2flash text,
cam2info text,
cam3flash text,
cam3info text,
cam4flash text,
cam4info text,
cam5flash text,
cam5info text,
cam6flash text,
cam6info text,
carrier text,
channels text,
codename text,
cpu text,
cpu_cores text,
cpu_freq text,
current_branch text,
depth text,
download_boot text,
gpu text,
height text,
image text,
install_method text,
kernel text,
maintainers text,
models text,
name text,
network2G text,
network3G text,
network4G text,
no_oem_unlock_switch text,
peripherals text,
ram text,
recovery_boot text,
release text,
screen text,
screen_ppi text,
screen_res text,
screen_tech text,
sdcard text,
soc text,
storage text,
tree text,
type text,
vendor text,
vendor_short text,
versions text,
width text,
wifi text,
custom_twrp_link text,
has_recovery_partition text,
before_install text,
required_bootloader text,
custom_twrp_codename text,
custom_unlock_cmd text,
network text,
project_spectrum text,
unlock_bootloader_guide text,
recovery_partition text,
root_method text,
gsm text,
is_unlockable text,
is_ab_device text,
install_variant text,
note_content text,
note_link text,
note_show text,
note_title text,
note_url text,
edl_boot text,
install_recovery_guide text,
project_spectrum_recovery text,
required_bootloader_link text,
multiple_versions_reason text,
format_on_upgrade text,
uses_lineage_recovery text,
custom_recovery_codename text,
custom_recovery_link text,
no_fastboot_boot text,
before_lineage_install text,
before_dd_recovery text,
uses_twrp text,
quirks text,
recovery_partition_name text,
before_recovery_install text,
firmware_update text,
variant text,
recovery_reboot text,
before_install_device_variants text,
is_retrofit_dynamic_partitions text,
needs_fastboot_boot text,
migrate_to text,
migrated_to text,
has_no_usb text,
flash_codename text,
flash_download_instructions text,
flash_extract_instructions text
)
''')
db.commit()


for dev in devs:
    sql = deviceToSqlInsert('devices/' + dev)
    #print(sql)
    cursor.execute(sql)
    #print("------------------------------------")
    db.commit()
    print(".", end="")
    sys.stdout.flush()
print()

print("the sqlite db should now be ready for use.")

db.close()


