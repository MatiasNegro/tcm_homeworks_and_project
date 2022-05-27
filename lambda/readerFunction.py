import logging
import json
import boto3
from boto3.dynamodb.conditions import Key
import pandas
import matplotlib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
ddb_client = boto3.client('dynamodb')
table = dynamodb.Table('DBresults')
table_list_races = dynamodb.Table('DBStartList')
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
                'race_name' : i['Event']['M']['Name']['S'],
                'race_date' : i['Event']['M']['StartTime']['M']['Date']['S'],
                'race_id' : i['event']['S'],
            }
            j += 1
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict=={}:
            response['body'] = 'Races not found'
        else:
            response['body'] = dict_json
        
        
    elif resource == 'download':
        #Getting the key
        key = prefix + event["queryStringParameters"]["filename"] + ".xml"
        try:
            race = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
            xml = race['Body'].read().decode('utf-8')
            response['body'] = xml
        except:
            response['body'] = 'error404'
        
        
    elif resource == 'list_classes':
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
                i=0
                for k in classResults:
                    dict['class'+str(i)] = {
                        'id' : classResults[k]['M']['Class']['M']['Id']['S'],
                        'Name' : classResults[k]['M']['Class']['M']['Name']['S']
                    }
                    i += 1
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict=={}:
            response['body'] = 'Error 404: Race not found'
        else:
            response['body'] = dict_json
        
        
    elif resource == 'results':
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
                                print(i['ClassResults']['M'][k]['M'][p]['M'])
                                idPlayer = i['ClassResults']['M'][k]['M'][p]['M']['Person']['M']['Id']['S']
                                surname = i['ClassResults']['M'][k]['M'][p]['M']['Person']['M']['Name']['M']['Family']['S']
                                name = i['ClassResults']['M'][k]['M'][p]['M']['Person']['M']['Name']['M']['Given']['S']
                                playerPosition = i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['Position']['S']
                                dict[playerPosition] = {
                                    'idPlayer' : idPlayer,
                                    'surname' : surname,
                                    'name' : name
                                }
        
        dict_json = json.dumps(dict, indent=4)
        dict_json = dict_json.split(', "ResponseMetadata":')
        dict_json = dict_json[0]
        if dict=={}:
            response['body'] = 'Error 404: Race not found'
        else:
            response['body'] = dict_json
        
    elif resource == 'download_start_list':
        id = event["queryStringParameters"]["id"]
        cl = event["queryStringParameters"]["class"]
        r = ddb_client.scan(
            TableName='DBStartList',
            AttributesToGet=[
                'idlist',
                'grid'
            ],
        )
        grid = ''
        for i in r['Items']:
            if (i['idlist']['S'] == (id+'-'+cl)):
                grid = i['grid']['S']
        if grid=='':
            response['body'] = '404'
        else:
            response['body'] = grid
    
    elif resource == 'split_time_jpeg':
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
                        i=0
                        for p in i['ClassResults']['M'][k]['M']:
                            i+=1
                            if 'PersonResult' in p:
                                person = i['ClassResults']['M'][k]['M'][p]['M']['Person']
                                k=0
                                for split in i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']:
                                    if 'SplitTime' in split:
                                        print(i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['SplitTime'+k]['M'])
        '''
                                        #splittimes = i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['SplitTimes']['M']
                                    dict[i] = {
                                        'player' : str(person),
                                        'splits' : str(splittimes)
                                    }
            string = str(dict)
            dict_json = json.dumps(dict, indent=4)
            dict_json = dict_json.split(', "ResponseMetadata":')
            dict_json = dict_json[0]
            if dict=={}:
                response['body'] = 'Error 404: Race not found'
            else:
                response['body'] = string
        '''

    else:
        response['body'] = 'Error 404: resource not found'
        
            
    return response