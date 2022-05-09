import logging
import base64
import boto3
import os
import xml.etree.ElementTree as ET
import re

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
j = 0

def lambda_handler(event, context):
    
    BUCKET_NAME = 'xmlresultgreco'
    bucket = s3_resource.Bucket(BUCKET_NAME)
    
    prefix = 'partite/'
    
    def name_control(file_name):
        for o in bucket.objects.all():
            if (prefix+file_name) == o.key:
                file_name = 'new_' + file_name
                file_name = name_control(file_name)
        return file_name
    
    files_name = []
    files_number = event['headers']['fileNumber']
    for i in range(int(files_number)):
        files_name.append(event['headers']['filename-'+str(i)])
    
    file_content = base64.b64decode(event['body'])
    
    # si passa da byte a string e si rimuove il flag di separazione dei file
    content_decoded = file_content.decode("utf-8")
    content_split = content_decoded.split('FLAGSEPARATORCODE')
    content_split.pop(len(content_split)-1)
    
    data = ""
    j = 0
    response['body'] = 'The following files have been uploaded:'
    
    # cicla per ogni file nella richiesta (string)
    for file in content_split:
        
        file_name = name_control(files_name[j])
        j += 1
        
        data = file.split('\r\n\r\n')
        data.pop(0)
        content = data[0]
        
        root = ET.fromstring(content)
        root.attrib.clear()
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')
        xmlstr = xmlstr.decode("utf8")
        content = re.sub(' xmlns:ns0="[^"]+"', '', xmlstr, count=1)
        content = content.replace('ns0:', '')
        
        try:
            s3_response = s3_client.put_object(Bucket=BUCKET_NAME, Key=(prefix+file_name), Body=content)
            logger.info('S3 Response: {}'.format(s3_response))
            response['body'] += "\n" + file_name
        
        except Exception as e:
            raise IOError(e)
            
    return response