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

    if resource == 'list_races':
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
                'race_name': i['Event']['M']['Name']['S'],
                'race_date': i['Event']['M']['StartTime']['M']['Date']['S'],
                'race_id': i['event']['S'],
            }
            j += 1
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict == {}:
            response['body'] = 'Races not found'
        else:
            response['body'] = dict_json

    elif resource == 'download':
        # Getting the key
        key = prefix + event["queryStringParameters"]["filename"] + ".xml"
        try:
            race = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
            xml = race['Body'].read().decode('utf-8')
            response['body'] = xml
        except:
            response['body'] = 'error404'


    elif resource =='list_classes':
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
                classResults = i['ClassResults']['M']
                i = 0
                for k in classResults:
                    dict['class'+str(i)] = {
                        'id': classResults[k]['M']['Class']['M']['Id']['S'],
                        'Name': classResults[k]['M']['Class']['M']['Name']['S']
                    }
                    i += 1
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict =={}:
            response['body'] = 'Error 404: Race not found'
        else:
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
        for i in r['Items']:
            if (i['event']['S'] == id):
                for k in i['ClassResults']['M']:
                    if (i['ClassResults']['M'][k]['M']['Class']['M']['Id']['S'] == cl):
                        for p in i['ClassResults']['M'][k]['M']:
                            if 'PersonResult' in p:
                                idPlayer = i['ClassResults']['M'][k]['M'][p]['M']['Person']['M']['Id']['S']
                                playerPosition = i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['Position']['S']
                                dict[playerPosition] = {
                                    'idPlayer': idPlayer
                                }

        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict =={}:
            response['body'] = 'Error 404: Race not found'
        else:
            response['body'] = dict_json

    else:
        response['body'] = 'Error 404: resource not found'


    return response
