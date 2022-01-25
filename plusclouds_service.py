import urllib.request

url_repo = 'https://raw.githubusercontent.com/plusclouds/vmOperations/main/plusclouds.py'
exec(urllib.request.urlopen(url_repo).read())
