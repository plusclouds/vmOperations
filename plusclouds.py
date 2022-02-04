import time
import platform
import distro
import os
import subprocess as sp
import requests
from hashlib import sha256
import urllib.request
import logging
from logging.handlers import RotatingFileHandler

#  This function takes filename as input, and then read it and return as a string variable

log_formatter = logging.Formatter(
    '%(levelname)s (%(lineno)d) ==> %(message)s')

logFile = '/var/log/plusclouds.log' if platform.system(
) == 'Linux' else 'C:\Windows\System32\winevt\Logs\plusclouds.log'

log_handler = RotatingFileHandler(
    logFile, mode='a', maxBytes=2*1024*1024, backupCount=1, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(log_handler)
app_log.info("")
app_log.info("============== Start of Execution at {}  =============".format(
    time.asctime()))


def file_read(fname):
    with open(fname, "r") as myfile:
        return myfile.readline().rstrip()


def execute_script(url):
    exec(urllib.request.urlopen(url).read())


def file_write(fname, data):
    file = open(fname, "w+")
    file.write(data)
    file.close()


def file_exists(fname):
    return os.path.exists(fname)


if platform.system() == 'Linux':
    # uuid of the vm assigned to uuid variable
    uuid = sp.getoutput('/usr/sbin/dmidecode -s system-uuid')
    # requests the information of the instance
    response = requests.get(
        'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid)).json()
    oldDisk = '0'
    total_disk = str(response['data']['virtualDisks']['data'][0]['total_disk'])
    hostname = response['data']['hostname']
    readablePassword = response['data']['password']
    password = sha256(readablePassword.encode()).hexdigest()

    # Password
    app_log.info(" ------  Password Check  ------")
    isChanged = False
    if (file_exists('/var/log/passwordlogs.txt')):
        oldPassword = file_read('/var/log/passwordlogs.txt')
        if (oldPassword != password):
            app_log.info(
                'Password in API is different. Setting isChanged variable to True')
            isChanged = True
            file_write("/var/log/passwordlogs.txt", password)
        else:
            app_log.info("Password is not changed in API.")
    else:
        app_log.info(
            "Password log file doesn't exist. Setting isChanged variable to True")
        isChanged = True
        file_write("/var/log/passwordlogs.txt", password)
    if (isChanged == True):
        app_log.info(
            'isChanged variable is set to True. Executing password change call')
        p = sp.Popen('passwd', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)
        stdout, stderr = p.communicate(
            input="{0}\n{0}\n".format(readablePassword).encode())
        if stderr:
            app_log.error(stderr)
        else:
            app_log.info('Password has been updated successfully')

    # Hostname
    app_log.info(" ------  Hostname Check  ------")
    oldHostname = file_read('/etc/hostname')
    if oldHostname != hostname:
        app_log.info('Hostname is different in API. Changing hostname in VM.')
        os.system('hostnamectl set-hostname {}'.format(hostname))
    else:
        app_log.info('Hostname is not changed in API')

    # Storage
    app_log.info(" ------  Storage Check  ------")
    url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/storage.py'
    if (file_exists('/var/log/disklogs.txt')):
        oldDisk = file_read('/var/log/disklogs.txt')
        if oldDisk != total_disk:
            app_log.info("Disk is changed from API. Executing storage.py")
            execute_script(url_repo)
        if file_exists("/var/log/isExtended.txt"):
            isExtended = file_read("/var/log/isExtended.txt")
            if isExtended == '1':
                app_log.info(
                    "Disk is extended before reboot. Executing storage.py to resize")
                execute_script(url_repo)
    else:
        app_log.info("Storage log file doesn't exist. Executing storage.py")
        execute_script(url_repo)

# Windows
if platform.system() == 'Windows':
    distroName = str(platform.system()) + '_' + str(platform.release())
    uuid = sp.check_output('wmic bios get serialnumber').decode().split('\n')[
        1].strip()
    # requests the information of the instance
    response = requests.get(
        'https://api.plusclouds.com/v2/iaas/virtual-machines/meta-data?uuid={}'.format(uuid)).json()
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

app_log.info("============== End of Execution at {}  =============".format(
    time.asctime()))
