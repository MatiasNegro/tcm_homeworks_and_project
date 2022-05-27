import logging
import json
import boto3
from boto3.dynamodb.conditions import Key
import matplotlib.pyplot as plt
import io
import base64

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
        dict={}
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
                        j=0
                        for p in i['ClassResults']['M'][k]['M']:
                            if 'PersonResult' in p:
                                person = i['ClassResults']['M'][k]['M'][p]['M']['Person']['M']
                                position = i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['Position']['S']
                                h=0
                                listSplit = []
                                for split in i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']:
                                    if 'SplitTime' in split:
                                        split = int(i['ClassResults']['M'][k]['M'][p]['M']['Result']['M']['SplitTime'+str(h)]['M']['Time']['S'])
                                        listSplit.append(split)
                                        h+=1
                                dict[j]={
                                    'person' : {
                                        'id' : person['Id']['S'],
                                        'Name' : person['Name']['M']['Given']['S'],
                                        'Family' : person['Name']['M']['Family']['S'],
                                        'Position' : position
                                    },
                                    'listSplit' : listSplit
                                }
                                j+=1
        
        lenx = len(dict[0]['listSplit'])
        x = [*range(1 , lenx+1, 1)]
        
        for p in dict:
            if dict[p]['person']['Position'] == str(1):
                splitFirst = dict[p]['listSplit']
        
        if len(splitFirst)==0:
            print('hai fuckappato')
        
        id = 'event'
        cl = 'class'
        plt.title('Race: '+id+'\nClass: '+cl)
        plt.ylabel('Time difference')
        plt.xlabel('Control')
        for person in dict:
            split = dict[person]['listSplit']
            y = []
            zip_object = zip(split, splitFirst)
            for list1_i, list2_i in zip_object:
                y.append(list1_i-list2_i)
        
            plt.plot(x, y, linestyle="", marker="o")
            plt.plot(x, y, color=plt.gca().lines[-1].get_color())
            plt.ylim(max(y)+10, 0)
            
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buf = buffer.getvalue()
        response['body'] = base64.b64encode(buf).decode('utf-8')
        response['headers'] = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'img/png'
        }
        
    else:
        response['body'] = 'Error 404: resource not found'
            
    return response