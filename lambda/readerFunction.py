import logging
import json
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
ddb_client = boto3.client('dynamodb')

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
    
    try:
        table = dynamodb.Table('DBresults')
        
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
                    'race_date' : i['Event']['M']['EndTime']['M']['Date']['S'],
                    'race_id' : i['event']['S'],
                }
                j += 1
            dict_json = json.dumps(dict, indent=4)
            dict_json = dict_json.split(', "ResponseMetadata":')
            dict_json = dict_json[0]
            response['body'] = dict_json
            
        elif(resource == 'download'):
            #Getting the key
            key = event["headers"]["filename"]
            #Query
            item = table.get_item(Key={'event': key})
            #Converting the item <dict> to json <string>
            item_json = json.dumps(item)
            item_json = item_json.split(', "ResponseMetadata":')
            item_json = item_json[0] + "}"
            #Item return when the query has been possile (statusCode:200)
            response['body'] = item_json
            
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
                if (i['event']['S'] == id):
                    dict = i['ClassResults']
            dict_json = json.dumps(dict, indent=4)
            dict_json = dict_json.split(', "ResponseMetadata":')
            dict_json = dict_json[0]
            response['body'] = dict_json
            
        elif(resource == 'results'):
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
                if (i['event']['S'] == id):
                    dict = i['ClassResults']
                    
            '''dict_json = json.dumps(dict, indent=4)
            dict_json = dict_json.split(', "ResponseMetadata":')
            dict_json = dict_json[0]
            response['body'] = dict_json'''
            
        else:
            response['body'] = 'Error 404: resource not found'
        
    except Exception as e:
        raise IOError(e)
            
    return response