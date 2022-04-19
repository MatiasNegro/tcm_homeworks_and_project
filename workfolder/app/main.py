from boto3.s3.transfer import S3Transfer
import boto3
#have all the variables populated which are required below
client = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=secret_key)
transfer = S3Transfer(client)
transfer.upload_file(filepath, bucket_name, folder_name+"/"+filename)

