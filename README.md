
# Virtual Machine Deployment Wizard Agent Script

This python script has been written in order to decrease virtual machine deployment times and costs. These scripts are supposed to be placed into Virtual Machines and get triggered by a cronjob within specific time periods. The script uses the UUID of the VM to access its information through the public API. Then it checks whether there are any changes in storage, hostname, and password and update the VM according to that.

### What Changes?

1. Storage Size
2. Hostname
3. Password

If the client make any change in the dashboard about the configurations that are listed below, this python script will detect changes, and apply these changes to the instance. Most of the essential parts of this code are executed on the fly. 

```
url_repo='https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
exec(urllib.request.urlopen(url_repo).read())
```

Alternatively, this module can be installed directly to the virtual machines and can directly be executed

#### To install this repository, please execute the following command:
```shell
pip install plusclouds-service
```

#### To execute this repository on Linux, please execute the following command:
```shell
sudo python3 -m plusclouds-service
```

#### To execute this repository on Windows, please execute the following command:
```shell
python -m plusclouds-service
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

### Folder Structure
<pre>
.
├── module_search
│   ├── ansible_operations.py
│   ├── callback_agent.py
│   ├── playbook-test.yml
│   └── service_search.py
├── service.<area>py
├── storage.<area>py
└── util
	└── ssh_keys
	    └── ssh_key_parser.py
</pre>
### Documentation

#### plusclouds.py<area>
- The driver code for all the checks such as storage, hostname, and password. Responsible for handling the response taken from the server.
#### storage.py<area>
- **create_file_if_not_exists(fname: str) -> None**
	- creates file in given "fname" path if not exists
- **create_folder_if_not_exists(dirname: str) -> None**
	- create folder in given "dirname" path if not exists
- **file_read(fname: str) -> str**
	- reads and returns the first line of file located in "fname"
- **file_write(fname: str, data: str) -> None**
	- writes "data" to file located in "fname" by overwriting the file contents. 
- **file_exists(fname: str) -> bool**
	- returns true if file_exists otherise returns false.
- **get_distribution() -> str**
	- returns the full distibution of the operating system. 
- **extend_disk() -> None:**
	- extends disk based on the current distribution
- **check_disk(uuid: str) -> None**
	- checks if there are any changes in the disk and if there are, executes extend_disk function based on the 		current OS
#### module_search
- **ansible_operations.py**
	- execute_playbook_script (directory: str)
		- executes the script in yml playbook.
	- download(url, dest_folder)
		- downloads downloadable contents in the given url and saves them to "dest_folder"
	- unzip(directory: str)
		- unzips the compressed file in given directory to the same directory
- **callback_agent.py**
	- class CallbackAgent
		- creates a callback agent in given url
- **service_search.py**
	- class PlusCloudsService
		- creates an instance of CallbackAgent and downloads service if missing. Initiates ansible and runs the playbook script.
### Supported Distributions

- Centos (7,8)
- Debian (9,10,11)
- Pardus (18.0,19.0)
- Ubuntu (16.04,18.04,19.04,19.10,20.04)
- Fedora30
- Windows Server (2016,2019)

### Performance Results

- %400 faster deployment time.
- %65 decreased bandwidth usage.
- %35 less errors during deployment.

### Author Information

- Talha Unsel - talha.unsel@plusclouds.com   
- Yigithan Saglam - saglamyigithan@gmail.com   
- Semih Yönet - semihyonet@gmail.com   
- Zekican Budin - zekican.budin@plusclouds.com   
