# Virtual Machine Deployment Wizard Agent Script

This python script has been written in order to decrease virtual machine deployment times and costs. These scripts are supposed to be placed into Virtual Machines and get triggered by a cronjob within specific time periods. The script uses the UUID of the VM to access its information through the public API. Then it checks whether there are any changes in storage, hostname, and password and update the VM according to that.

### What Changes?

1. Storage Size
2. Hostname
3. Password

If the client make any change in the dashboard about the configurations that are listed below, this python script will detect changes, and apply these changes to the instance.
Most of the essential parts of this code are executed on the fly. The code is not stored in VM instances but gets fetched from the repository and gets executed in RAM.

```
url_repo='https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
exec(urllib.request.urlopen(url_repo).read())
```

#### To install this repository, please execute the following command:
```shell
pip install -i https://test.pypi.org/simple/ vm-operations==0.0.1
```

#### To execute this repository, please execute the following command:
```shell
sudo python3 -m vm-operations
```

### Benefits of this approach

1. Maintanence of the code for the future. You are supposed to update the github repository instead of changing the scripts in each Virtual Machine Image.

### Requirements

- Python3
- Python3 distro package
- Python3 request package

### Notes

- Logging is limited to two files that are 2MB each. You can change the size and count of log files by changing maxBytes, and backupCount input variables in RotatingFileHandler call.
- For the hosname and password policy in Windows Servers, you can check the following links
  - Password: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements
  - Hostname: https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/naming-conventions-for-computer-domain-site-ou

### Supported Distributions

- Centos (7,8)
- Debian (9,10,11)
- Pardus (18.0,19.0)
- Ubuntu (16.04,18.04,19.04,19.10,20.04)
- Fedora30
- Windows Server (2016,2019)

### Performance Results

- %400 faster deployment time.
- Bandwidth usage decrease %180.
- Errors during deployment decrase %35.

### Author Information

- Talha Unsel - talha.unsel@plusclouds.com   
- Yigithan Saglam - saglamyigithan@gmail.com   
- Semih Yönet - semihyonet@gmail.com   
- Zekican Budin - zekican.budin@plusclouds.com   
