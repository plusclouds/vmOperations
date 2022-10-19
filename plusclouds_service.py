from urllib.request import urlopen

url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
exec(urlopen(url_repo).read())