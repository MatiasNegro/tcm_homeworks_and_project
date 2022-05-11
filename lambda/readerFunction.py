import logging
import json
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
ddb_client = boto3.client('dynamodb')
table = dynamodb.Table('DBresults')
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
BUCKET_NAME = 'xmlresultgreco'
bucket = s3_resource.Bucket(BUCKET_NAME)
prefix = 'partite/'

response  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

def lambda_handler(event, context):
    
    resource = event["resource"]
    resource = resource.replace('/','')
    response['body'] = ''


    
    if(resource == 'list_races'):
        
        dict = {}
        r = ddb_client.scan(
            TableName='DBresults',
            AttributesToGet=[
                'event',
                'Event'
            ],
        )
        j = 0
        for i in r['Items']:
            dict[j] = {
                'race_name' : i['Event']['M']['Name']['S'],
                'race_date' : i['Event']['M']['StartTime']['M']['Date']['S'],
                'race_id' : i['event']['S'],
            }
            j += 1
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        response['body'] = dict_json
        
        
    elif(resource == 'download'):
        
        #Getting the key
        key = prefix + event["headers"]["filename"]
        #Query
        try:
            race = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
            xml = race['Body'].read().decode('utf-8')
            print(xml)
            response['body'] = xml
        except:
            response['body'] = '404'
        
    elif(resource == 'list_classes'):
        
        dict = {}
        id = event["queryStringParameters"]["id"]
        r = ddb_client.scan(
            TableName='DBresults',
            AttributesToGet=[
                'event',
                'ClassResults'
            ],
        )
        j = 0
        for i in r['Items']:
            print(i['event']['S'])
            if (i['event']['S'] == id):
                dict = i['ClassResults']
                print(dict)
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        response['body'] = dict_json
        
        
    elif(resource == 'results'):
        
        dict = {}
        id = event["queryStringParameters"]["id"]
        cl = event["queryStringParameters"]["class"]
        r = ddb_client.scan(
            TableName='DBresults',
            AttributesToGet=[
                'event',
                'ClassResults'
            ],
        )
        j = 0
        for i in r['Items']:
            if (i['event']['S'] == id):
                for k in i['ClassResults']['M']:
                    for l in i['ClassResults']['M'][k]['L']:
                        print(l['M']['Class']['M']['Id']['S'])
                
                
        '''dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        response['body'] = dict_json'''
        
        
    else:
        response['body'] = 'Error 404: resource not found'
        
            
    return response