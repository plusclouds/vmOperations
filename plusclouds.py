import time
import platform
import distro
import os
import subprocess as sp
import requests
from hashlib import sha256
import urllib.request

#  This function takes filename as input, and then read it and return as a string variable


def file_read(fname):
    with open(fname, "r") as myfile:
        return myfile.readline().rstrip()


def execute_script(url):
    exec(urllib.request.urlopen(url).read())


if platform.system() == 'Linux':
    distroName = str(distro.linux_distribution(full_distribution_name=False)[
                     0]) + str(distro.linux_distribution(full_distribution_name=False)[1])
    distroName = str(distroName.capitalize())
    # uuid of the vm assigned to uuid variable
    uuid = sp.getoutput('/usr/sbin/dmidecode -s system-uuid')
    # requests the information of the instance
    response = requests.get(
        'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid))
    person_dict = response.json()  # json to dict
    oldDisk = '0'
    total_disk = person_dict['data']['virtualDisks']['data'][0]['total_disk']
    total_disk = str(total_disk)
    hostname = person_dict['data']['hostname']
    password = person_dict['data']['password']
    readablePassword = password
    password = sha256(readablePassword.encode()).hexdigest()

    # Password
    fileFlag = os.path.exists('/var/log/passwordlogs.txt')
    url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/password.py'
    if (fileFlag == True):
        oldPassword = file_read('/var/log/passwordlogs.txt')
        if (oldPassword != password):
            execute_script(url_repo)
    else:
        execute_script(url_repo)

    # Hostname
    oldHostname = file_read('/etc/hostname')
    if oldHostname != hostname:
        url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
        execute_script(url_repo)

    # Storage
    isDiskLog = os.path.exists('/var/log/disklogs.txt')
    url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/storage.py'
    if (isDiskLog == True):
        oldDisk = file_read('/var/log/disklogs.txt')
        if oldDisk != total_disk:
            execute_script(url_repo)
        if os.path.exists("/var/log/isExtended.txt") == True:
            isExtended = file_read("/var/log/isExtended.txt")
            if isExtended == '1':
                execute_script(url_repo)
    else:
        execute_script(url_repo)

# Windows
if platform.system() == 'Windows':
    distroName = str(platform.system()) + '_' + str(platform.release())
    uuid = sp.check_output('wmic bios get serialnumber').decode().split('\n')[
        1].strip()
    # requests the information of the instance
    response = requests.get(
        'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid))
    response = response.json()  # json to dict
    password = response['data']['password']
    hashed_password = sha256(password.encode()).hexdigest()
    hostname = response['data']['hostname']

    # Password

    isChanged = False
    fileFlag = os.path.exists(
        'C:\Windows\System32\winevt\Logs\passwordlog.txt')
    if (fileFlag == True):
        oldPassword = file_read(
            'C:\Windows\System32\winevt\Logs\passwordlog.txt')
        if (oldPassword != hashed_password):
            isChanged = True
            print('Password has been changed since last execution')
            f = open("C:\Windows\System32\winevt\Logs\passwordlog.txt", "w+")
            f.write(password)
            f.close()
        else:
            print('Password has not been changed')
    else:
        isChanged = True
        f = open("C:\Windows\System32\winevt\Logs\passwordlog.txt", "w+")
        f.write(hashed_password)
        f.close()
    if (isChanged == True):
        sp.call("net users" + " Administrator " + password, shell=True)

    # Hostname

    current_hostname = sp.check_output(
        'hostname').decode().split('\n')[0].strip()
    hostname = hostname if len(hostname) <= 15 else hostname[0:15]
    if hostname != current_hostname:
        sp.call(["powershell", "Rename-Computer -NewName " + hostname], shell=True)

    # Disk

    p = sp.Popen(["diskpart"], stdout=sp.PIPE,
                 stdin=sp.PIPE, stderr=sp.PIPE)
    commands = ['select disk 0\n', 'select vol 2\n', 'extend\n', 'exit\n']
    for command in commands:
        p.stdin.write(bytes(command, 'utf-8'))
        time.sleep(.3)

    # WinRM toggle

    def setup_winrm():
        file_loc = sp.check_output('powershell.exe $env:temp')
        file_loc = file_loc.decode("utf-8").split()[0]

        file = open(file_loc + '\\ansible_setup.ps1', 'w+')
        file.write('''
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
        $file = "$env:temp\\ConfigureRemotingForAnsible.ps1"
        (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
        powershell.exe -ExecutionPolicy ByPass -File $file
        ''')

        file.close()

        p = sp.Popen(['powershell.exe', file_loc +
                      '\\ansible_setup.ps1'], stdout=sp.PIPE)
        out, err = p.communicate()
        print(out)
        if err:
            print(err)

    def is_winrm_set():
        output = sp.check_output(
            'powershell.exe winrm enumerate winrm/config/Listener')
        if len(output.decode("utf-8").split('Listener')) != 3:
            return False
        output = output.decode("utf-8").split('Listener')[2].split('\r\n    ')
        winrm_listener = dict([i.split(' = ') for i in output[1:]])

        return (winrm_listener['Enabled'] == 'true' and winrm_listener['CertificateThumbprint'] and winrm_listener['ListeningOn'])

    uuid = sp.check_output('wmic bios get serialnumber ').decode().split('\n')[
        1].strip()

    winrm_api_status = False
    if 'winrm_enabled' in response['data']:
        winrm_api_status = response['data']['winrm_enabled']
    is_winrm_running = True if sp.check_output(
        'powershell.exe Get-Service winrm').decode("utf-8").split()[6].lower() == "running" else False

    if winrm_api_status:
        if not is_winrm_running:
            p = sp.Popen('powershell.exe Start-Service winrm')
        if not is_winrm_set():
            setup_winrm()
    else:
        if is_winrm_running:
            p = sp.Popen('powershell.exe Stop-Service winrm')
