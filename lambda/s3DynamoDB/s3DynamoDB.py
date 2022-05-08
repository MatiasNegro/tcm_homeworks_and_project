import boto3
import json
import xml_parser as xp
from xml.etree.ElementTree import fromstring, ElementTree, XMLParser
from boto3.dynamodb.types import TypeSerializer

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    #Getting file from bucketS3
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    #THe file is an xml, we need the json
    xml_obj = s3_client.get_object(Bucket = bucket, Key = file_name)['Body'].read().decode('utf-8')
    xml_str = xml_obj#[(108):len(xml_obj) - 38]
    tree = ElementTree(fromstring(xml_str))

    root = tree.getroot()
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