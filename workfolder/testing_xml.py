import xmltodict
import json

with open('workfolder/ResultList1.xml', 'r') as myfile:
    obj = xmltodict.parse(myfile.read())
print(json.dumps(obj))