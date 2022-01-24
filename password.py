import requests
import json
import os
import subprocess as sp
from hashlib import sha256

# This function takes filename as input, and then read it and return as a string variable


def file_read(fname):
    with open(fname, "r") as myfile:
        return myfile.readline().rstrip()  # read the password from file


def file_write(fname, data):
    file = open(fname, "w+")
    file.write(data)
    file.close()


def file_exists(fname):
    return os.path.exists(fname)


# uuid of the vm assigned to uuid variable
uuid = sp.getoutput('/usr/sbin/dmidecode -s system-uuid')
# requests the information of the instance
response = requests.get(
    'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid))
readablePassword = response.json()['data']['password']
password = sha256(readablePassword.encode()).hexdigest()
isChanged = False

if (file_exists('/var/log/passwordlogs.txt')):
    oldPassword = file_read('/var/log/passwordlogs.txt')
    if (oldPassword != password):
        app_log.info(
            'Password in API is different. Setting isChanged variable to True')
        isChanged = True
        file_write("/var/log/passwordlogs.txt", password)
    else:
        app_log.info('Password has not been changed')
else:
    app_log.info(
        'Password log file does NOT exist. Setting isChanged True to change password in next step')
    isChanged = True
    file_write("/var/log/passwordlogs.txt", password)

if (isChanged == True):
    app_log.info(
        'isChanged variable is set to True. Executing password change call')
    cmd = "bash -c \"echo -e '{}\\n{}' | passwd root\"".format(
        readablePassword, readablePassword)
    sp.check_call(cmd, shell=True)
    app_log.info('Password has been updated successfully')
