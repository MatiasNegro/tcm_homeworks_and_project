import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #Table definition
    table = dynamodb.Table('my_test_table')
    #Getting the key
    key = event["queryStringParameters"]["key"]
    #Query
    item = table.get_item(Key={'Name': str(key)})
    #Converting the item <dict> to json <string>
    item_json = json.dumps(item)
    #Item return when the query has been possile (statusCode:200)
    return{
        'statusCode': 200,
            'body': item_json
        }