import requests
import json
import os
import subprocess as sp
import fnmatch
import distro

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


distroName = str(distro.linux_distribution(full_distribution_name=False)[
    0]) + str(distro.linux_distribution(full_distribution_name=False)[1])


def extend_disk():
    try:
        if distroName in ['ubuntu18.04']:
            xvdaCount = len(fnmatch.filter(os.listdir('/dev'), 'xvda*'))
            gdisk_command = "bash -c \"echo -e 'd\n{}\nn\n\n\n\n\nw\nY\nY\n' | sudo gdisk /dev/xvda\"".format(
                str(xvdaCount-1))
            sp.check_call(gdisk_command, shell=True)
            cmd = "bash -c \"echo -e 'd\n\nn\n\n\n\nN\nw\n' | sudo fdisk /dev/xvda\""

        if distroName in ['centos7', 'centos8', 'debian17.5', 'pardus19.0', 'ubuntu16.04']:
            cmd = "bash -c \"echo -e 'd\n\nn\n\n\n\n\nw\n' | sudo fdisk /dev/xvda\""

        if distroName in ['debian9', 'debian10', 'debian11', 'fedora30']:
            cmd = "bash -c \"echo -e 'd\n\nn\n\n\n\n\nN\nw\n' | sudo fdisk /dev/xvda\""

        if distroName in ['ubuntu19.04', 'ubuntu19.10', 'ubuntu20.04']:
            cmd = "bash -c \"echo -e 'd\n\nn\n\n\n\nN\nw\n' | sudo fdisk /dev/xvda\""
            cmd = "bash -c \"echo -e 'd\n\nn\n\n\n\nN\nw\n' | sudo fdisk /dev/xvda\""

        sp.check_call(cmd, shell=True)

    except Exception:
        pass

    file_write("/var/log/isExtended.txt", "1")
    print("System will be rebooted.")
    os.system('sudo reboot')


xvdaCount = str(len(fnmatch.filter(os.listdir('/dev'), 'xvda*')) - 1)


if distroName in ['centos7', 'centos8', 'fedora30']:
    resizeCall = 'sudo xfs_growfs /dev/xvda{}'.format(xvdaCount)
else:
    resizeCall = 'sudo resize2fs /dev/xvda{}'.format(xvdaCount)

# uuid of the vm assigned to uuid variable
uuid = sp.getoutput('/usr/sbin/dmidecode -s system-uuid')
try:
    response = requests.get(
        'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid), timeout=3)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)
response_dict = response.json()  # json to dict
total_disk = str(response_dict['data']
                 ['virtualDisks']['data'][0]['total_disk'])

oldDisk = '0'

isDiskLog = os.path.exists('/var/log/disklogs.txt')
if (isDiskLog == True):
    oldDisk = file_read('/var/log/disklogs.txt')
    f = open("/var/log/disklogs.txt", "w+")
    f.write(total_disk)
    f.close()
else:
    file_write("/var/log/disklogs.txt", total_disk)

if (total_disk != '10240'):
    if (not file_exists('/var/log/isExtended.txt')) or (oldDisk != total_disk):
        extend_disk()

else:
    print('No need for disk extend.')
    file_write("/var/log/isExtended.txt", '0')

isExtended = file_read("/var/log/isExtended.txt")
if (isExtended == '1'):
    os.system(resizeCall)
    file_write("/var/log/isExtended.txt", '0')
