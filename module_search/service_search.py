import urllib.request
import os
import requests

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")+".zip"  # be careful with file names
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

def unzip(directory: str):
    print("Unzipping in dir: ", directory)
    os.system("apt-get install unzip")

    print(os.system("unzip -o "+directory))

    print("Execution complete!")

def execute_playbook_script(directory: str):
    print("executing Playbook in dir: ", directory)

    print(os.system("ansible-playbook "+directory))

    print("Execution complete!")

class plusclouds_service:
    def __init__(self, service_name: str, service_url: str):
        self.service_name = service_name

        self.download_path = "./"+service_name

        self.is_downloaded = False

        self.is_initiated = False

        self.service_url = service_url


    def download_module(self):
        if self.is_downloaded:
            raise Exception("Already downloaded!")

        self.is_downloaded = True
        return download(self.service_url, self.download_path)

    def initiate_ansible(self):
        if not self.is_downloaded:
            self.download_module()
        execute_playbook_script("index.yml")
        self.is_initiated = True

    def run(self):
        path = self.download_module()
        unzip(path)
        self.initiate_ansible()
