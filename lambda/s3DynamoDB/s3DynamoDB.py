import boto3
import json
import xml_parser as xp
import xml.etree.ElementTree as ET
from boto3.dynamodb.types import TypeSerializer
import copy

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def class_result_parser(root): 
    '''
    Prende in ingresso una root del documento xml e restituisce le classi dentro un unico tag <ClassResults> per garantire la compatibilità con dynamodb ed evitare la sovrascrittura dei <ClassResult>
    '''
    class_results_base = ET.fromstring("<ClassResults></ClassResults>")
    result_list = ET.fromstring("<ResultList></ResultList>")
    c_r_s = copy.deepcopy(class_results_base)
    r_l = copy.deepcopy(result_list)
    event = copy.deepcopy(ET.ElementTree(root.find("Event"))).getroot()
    r_l.append(event)
    index_class : int = 0
    index_person : int = 0
    index_split_time : int = 0
    for i in root.findall("ClassResult"):
        i.tag = "ClassResult" + str(index_class)
        index_class += 1
        for j in i.findall("PersonResult"):
            j.tag = "PersonResult" + str(index_person)
            split_times = j.find('Result').findall('SplitTime')
            for k in split_times:
                k.tag = "SplitTime" + str(index_split_time)
                index_split_time += 1
            index_split_time = 0
            index_person += 1
        index_person : int = 0
        c_r_s.append(i)
    r_l.append(c_r_s)
    return r_l

def lambda_handler(event, context):
    
    #Getting file from bucketS3
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    #THe file is an xml, we need the json
    xml_obj = s3_client.get_object(Bucket = bucket, Key = file_name)['Body'].read().decode('utf-8')
    xml_str = xml_obj#[(108):len(xml_obj) - 38]
    tree = ET.fromstring(xml_str)

    root = tree
    root = class_result_parser(tree)

    xmldict = xp.XmlDictConfig(root)

    #Json from xml
    to_db = json.dumps(xmldict)
    to_db_dict = json.loads(to_db)
    
    #Creation of the key as Name of the event + Date of the event
    name = to_db_dict["Event"]["Name"] + to_db_dict["Event"]["StartTime"]["Date"]
    table = dynamodb.Table('DBresults')
    
    #Serialization of the data
    serializer = TypeSerializer()
    to_db_dict_serialized = serializer.serialize(to_db_dict)
    
    #Insert of the Item inside the db
    response = table.put_item(Item = {**{"event": name}, **to_db_dict})
    
    print(response)