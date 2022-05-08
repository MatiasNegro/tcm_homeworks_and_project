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
    
    mod = event['headers']['mod']
    response['body'] = ''
    
    try:
        table = dynamodb.Table('DBresults')
        
        if(mod == 'read'):

            primary_keys= []
            count = 0
            r = ddb_client.scan(
                TableName='DBresults',
                AttributesToGet=[
                    'event',
                ],
            )
            count += r['Count']
            for i in r['Items']:
                primary_keys.append(i['event']['S'])
            for key in primary_keys:
                response['body'] += key + '\n'
            
        elif(mod == 'download'):
            #Table definition
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
            
        else:
            response['body'] = 'Error 404: "mod" header not found'
        
    except Exception as e:
        raise IOError(e)
            
    return response