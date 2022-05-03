import requests
import glob
import os

os.chdir("Result_Of_Simulation")
url = ''

files = []
for file in glob.glob("*.xml"):
    files.append({file : open(file, 'r')})

print(dict(files))

#response = requests.post(url= url, headers='file-name', files=dict(files))