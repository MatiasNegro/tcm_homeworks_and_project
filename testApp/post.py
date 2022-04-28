import requests

def sendPost(url, file_url):
    
    header_file_name = {'file-name': 'ResultList1.xml'}
    file = {'file': open(file_url, 'r')}
    r = requests.post(url, files=file, headers = header_file_name)
    print(r.text)

url = 'https://f0zfgut2oc.execute-api.us-east-1.amazonaws.com/dev/upload'
file_url = 'workfolder/ResultList1.xml'
sendPost(url = url, file_url = file_url)