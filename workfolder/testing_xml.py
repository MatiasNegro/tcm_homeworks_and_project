import pandas_r_xml
import json

xml_file = pandas_r_xml.read_xml("workfolder/ResultList1.xml")
json_obj = xml_file.to_json()
json_dic = json.loads(json_obj)
print(json_dic)