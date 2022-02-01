# Virtual Machine Deployment Wizard Agent Script

This python script has been written in order to decrease virtual machine deployment times and costs. These scripts are supposed to be placed into Virtual Machines and get triggered by a cronjob within specific time periods. The script uses the UUID of the VM to access its information through the public API. Then it checks whether there are any changes in storage, hostname, and password and update the VM according to that.

### What Changes?

1. Storage size.
2. Hostname changes.
3. Password changes.

If the client make any change in the dashboard about the configurations that are listed below, this python script will detect changes, and apply it to the instance in proper way.
Most of the essential parts of this code are executed on the fly. The code is not stored in VM instances but gets fetched and executed in RAM.

```
url_repo='https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
exec(urllib.request.urlopen(url_repo).read())
```

### Benefits of this approach

1. Maintanence of the code for the future. You are supposed to update the github repository instead of changing the scripts in each Virtual Machine Image.

### Requirements

- Python3
- Python3 distro package
- Python3 request package

### Notes

- Logging is limited to two files that are 2MB each. You can change the size and count of log files by changing maxBytes, and backupCount input variables in RotatingFileHandler call.
- For the password policy in Windows Servers, you can check the following link: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements

### Supported Distributions

- Centos7
- Debian10
- Debian11
- Pardus18
- Debian9
- Fedora30
- Pardus19.0
- Ubuntu16.04
- Ubuntu18.04
- Ubuntu19.04
- Ubuntu19.10
- Ubuntu20.04

- Windows Server 2019
- Windows Server 2016

### Performance Results

- %400 faster deployment time.
- Bandwidth usage decrease %180.
- Errors during deployment decrase %35.

### Author Information

Talha Unsel - talha.unsel@plusclouds.com
Yigithan Saglam - saglamyigithan@gmail.com
