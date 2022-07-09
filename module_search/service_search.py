import urllib.request
import os
import requests

import module_search.callback_agent


def download(url: str, dest_folder: str):
	if not os.path.exists(dest_folder):
		os.makedirs(dest_folder)  # create folder if it does not exist

	filename = url.split('/')[-1].replace(" ", "_") + ".zip"  # be careful with file names
	file_path = os.path.join(dest_folder, filename)

	r = requests.get(url, stream=True)
	if r.ok:
		print("saving to", os.path.abspath(file_path))
		with open(file_path, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024 * 8):
				if chunk:
					f.write(chunk)
					f.flush()
					os.fsync(f.fileno())

		return file_path
	else:  # HTTP status code 4XX/5XX
		print("Download failed: status code {}\n{}".format(r.status_code, r.text))
		return ""


def unzip(directory: str):
	print("Unzipping in dir: ", directory)

	if not os.path.exists(directory):
		return False

	os.system("apt-get install unzip")

	print(os.system("unzip -o " + directory))

	print("Execution complete!")

	return True


def execute_playbook_script(directory: str):
	print("executing Playbook in dir: ", directory)

	if not os.path.exists(directory):
		return False

	print(os.system("ansible-playbook -i hosts " + directory))  # haven't tried with -i hosts flag
	print("Execution complete!")

	return True


class plusclouds_service:
	def __init__(self, service_name: str, service_url: str, callback_ansible_url: str, callback_service_url: str):
		self.service_name = service_name

		self.download_path = "./services" + service_name

		self.is_downloaded = False

		self.is_initiated = False

		self.service_url = service_url

		self.callback_ansible_url = callback_ansible_url

		self.callback_service_url = callback_service_url

		self.callback_agent = module_search.callback_agent.CallbackAgent(self.callback_service_url)

	def download_module(self):
		if self.is_downloaded:
			raise Exception("Already downloaded!")

		self.is_downloaded = True
		return download(self.service_url, self.download_path)

	def initiate_ansible(self):
		if not self.is_downloaded:
			self.download_module()

		execute_playbook_script("install.yml")
		self.is_initiated = True

	def run(self):
		self.callback_agent.downloading("Downloading starting")
		try:
			path = self.download_module()
		except requests.exceptions.ConnectionError as e:
			self.callback_agent.failed("Download failed ")
			return

		else:
			self.callback_agent.initiating("Download completed, starting unzipping")

		if not unzip(path):
			self.callback_agent.failed("Unzip failed")
			return
		else:
			self.callback_agent.initiating("Playbook Execution starting.")

		self.initiate_ansible()
		self.callback_agent.completed("Completed!")
