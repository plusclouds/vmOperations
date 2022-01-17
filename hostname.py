import requests
import json
import os
import subprocess as sp

# This function takes filename as input, and then read it and return as a string variable


def file_read(fname):
    with open(fname, "r") as myfile:
        return myfile.readline().rstrip()  # read the hostname from file


# uuid of the vm assigned to uuid variable
uuid = sp.getoutput('/usr/sbin/dmidecode -s system-uuid')
# requests the information of the instance
response = requests.get(
    'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid))
person_dict = response.json()
hostname = person_dict['data']['hostname']
oldHostname = file_read('/etc/hostname')
isChanged = False
fileFlag = os.path.exists('/etc/hostname')

if (oldHostname != hostname):
    os.system('hostnamectl set-hostname {}'.format(hostname))
