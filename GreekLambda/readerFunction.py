import logging
import base64
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

response  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

def lambda_handler(event, context):
    
    BUCKET_NAME = 'xmlresultgreco'
    bucket = s3_resource.Bucket(BUCKET_NAME)
    mod = event['headers']['mod']
    response['body'] = ''
    
    try:
        if(mod == 'read'):
            fileKeys = []
            for o in bucket.objects.all():
                if("partite/" in o.key):
                    fileKeys.append(o.key)
            for key in fileKeys:
                response['body'] += key + '\n'
                
        elif(mod == 'download'):
            found = False
            filekey = event['headers']['filename']
            for o in bucket.objects.all():
                if('partite/' + filekey == o.key):
                    found = True
                    file = o.get()['Body'].read().decode('utf-8') 
                    response['body'] = file
            if(found == False):
                response['body'] = '404'
        
        else:
            response['body'] = 'Error 404: "mod" header not found'
        
    except Exception as e:
        raise IOError(e)
            
    return response