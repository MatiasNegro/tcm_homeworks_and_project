import logging
import base64
import boto3
import os

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

    file_name = event['headers']['file-name']
    file_content = base64.b64decode(event['body'])
    
    BUCKET_NAME = os.environ['BUCKET_NAME']
    bucket = s3_resource.Bucket(BUCKET_NAME)
    
    prefix = 'partite/'
    changed_name = False
    
    def name_control(file_name, prefix, bucket):
        for o in bucket.objects.all():
            if (prefix+file_name) == o.key:
                changed_name = True
                file_name = 'new_' + file_name
                file_name = name_control(file_name, prefix, bucket)
        return file_name
    
    file_name = name_control(file_name, prefix, bucket)
    
    try:
        s3_response = s3_client.put_object(Bucket=BUCKET_NAME, Key=(prefix+file_name), Body=file_content)   
        logger.info('S3 Response: {}'.format(s3_response))
        if(changed_name):
            response['body'] = 'Your file has been uploaded'
        else:
            response['body'] = 'Your file has been uploaded, name already existing: new name = ' + file_name
        return response

    except Exception as e:
        raise IOError(e)