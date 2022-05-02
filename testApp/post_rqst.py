import requests

def sendPost(url, file_url):
    file = {'file': open(file_url, 'rb')}
    r = requests.post(url, files= file, headers = {'file-name': 'ResultList1.xml'})
    print(r.text)
 

url = 'https://f0zfgut2oc.execute-api.us-east-1.amazonaws.com/dev/upload'#input('Paste the url for the first request: ')
file_url = 'workfolder\ResultList1.xml'
sendPost(url= url, file_url= file_url)
