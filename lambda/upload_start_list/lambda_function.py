import logging
import json
import base64
import boto3
import xml.etree.ElementTree as ET
import re
from xmlParser import XmlDictConfig

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DBStartList')

response = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

def lambda_handler(event, context):
    
    resource = event["resource"]
    resource = resource.replace('/', '')
    response['body'] = ''
    
    if resource == 'upload_start_list':
        
        file_content = base64.b64decode(event["body"])
        file_content = file_content.decode("utf-8")
        file_content = re.sub(' xmlns="[^"]+"', '', file_content, count=1)
        
        root = ET.fromstring(file_content)
        root.attrib.clear()
        eventName = event['headers']['fileName']
        
        for classstart in root:
            if classstart.tag != 'Event':
                classId = classstart[0][0].text
                grid = {}
                i = 1
                for personstart in classstart:
                    if personstart.tag == 'PersonStart':
                        personstartdict = XmlDictConfig(personstart)
                        grid[i] = personstartdict
                        i += 1
                t = table.put_item(Item = {**{"idlist": eventName+'-'+classId}, **{"class": classId}, **{"grid": str(grid)} })
                code = t['ResponseMetadata']['HTTPStatusCode']
                if code != 200:
                    brake
                
        if code==200:
            response['body'] = '200'
        else:
            response['body'] = t
    
    else:
        response['body'] = 'Error 404: resource not found'
    
    return response