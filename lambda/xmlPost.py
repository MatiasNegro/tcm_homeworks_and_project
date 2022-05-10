import logging
import base64
import boto3
import os
import xml.etree.ElementTree as ET
import re
import copy

## dichiarazione variabili globali
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

BUCKET_NAME = 'xmlresultgreco'
bucket = s3_resource.Bucket(BUCKET_NAME)
prefix = 'partite/'
j = 0

response  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

def class_result_parser(root): 
    '''
    Prende in ingresso una root del documento xml e restituisce le classi dentro un unico tag <ClassResults> per garantire la compatibilità con dynamodb ed evitare la sovrascrittura dei <ClassResult>
    '''
    class_results_base = ET.fromstring('<ClassResults></ClassResults>')
    result_list = ET.fromstring('<ResultList></ResultList>')
    c_r_s = copy.deepcopy(class_results_base)
    r_l = copy.deepcopy(result_list)
    event = copy.deepcopy(ET.ElementTree(root.find("Event"))).getroot()
    r_l.append(event)
    for i in root.findall("ClassResult"):
        c_r_s.append(i)
    r_l.append(c_r_s)
    return r_l

def name_control(file_name):
    '''
    Controllo il bucket per vedere se il nome del file è già presente, nel caso cambia nome
    '''
    for o in bucket.objects.all():
        if (prefix+file_name) == o.key:
            file_name = 'new_' + file_name
            file_name = name_control(file_name)
    return file_name


def lambda_handler(event, context):
    
    # identificazione tipo di risorsa chiamata
    resource = event["resource"]
    resource = resource.replace('/','')
    response['body'] = ''
    
    # in base al tipo di risorsa esegui funzioni diverse
    if resource == 'upload':
        
        # prende il numero totale dei file nella POST request e immagazzina i nomi in una list
        files_name = []
        files_number = event['headers']['fileNumber']
        for i in range(int(files_number)):
            files_name.append(event['headers']['filename-'+str(i)])
        
        # estrae il body che contiene i file separati dal flag FLAGSEPARATORCODE
        file_content = base64.b64decode(event['body'])
        
        # si passa da byte a string e si rimuove il flag di separazione dei file
        content_decoded = file_content.decode("utf-8")
        content_split = content_decoded.split('FLAGSEPARATORCODE')
        content_split.pop(len(content_split)-1)
        
        data = ""
        global j
        j = 0
        response['body'] = 'The following files have been uploaded:'
        
        # cicla per ogni file nella richiesta (string)
        for file in content_split:
            
            # controlla che il file sia già presente nel bucket
            file_name = name_control(files_name[j])
            j += 1
            
            # pulizia del file dai metadati presenti all'inizio aggiunti dalla POST request
            data = file.split('\r\n\r\n')
            data.pop(0)
            content = data[0]
            
            # conversione da string ad xml
            root = ET.fromstring(content)
            root.attrib.clear()
            
            # inserimento dei <ClassResult> in un unico <ClassResults> per preparare l'inserimento nel database
            root = class_result_parser(root)
            
            # rimozione del namespace
            xmlstr = ET.tostring(root, encoding='utf8', method='xml')
            xmlstr = xmlstr.decode("utf8")
            content = re.sub(' xmlns:ns0="[^"]+"', '', xmlstr, count=1)
            content = content.replace('ns0:', '')
            
            # inserimento nel bucket
            try:
                s3_response = s3_client.put_object(Bucket=BUCKET_NAME, Key=(prefix+file_name), Body=content)
                logger.info('S3 Response: {}'.format(s3_response))
                response['body'] += "\n" + file_name
            
            except Exception as e:
                raise IOError(e)
                
    elif(resource == 'register_race'):
        
        # all'interno di claims ci sono gli attributi di chi esegue la request
        username = event["requestContext"]["authorizer"]["claims"]["cognito:username"]
        email = event["requestContext"]["authorizer"]["claims"]["email"]
        
        # parametri obbligatori per la registrazione di una gara
        race_name = event["queryStringParameters"]["race_name"]
        race_date = event["queryStringParameters"]["race_date"]
        # individuazione parametri non obbligatori
        if (len(event["queryStringParameters"])>2):
            print('ci sono più parametri')
        
        # INSERIRE CODICE PER LA GENERAZIONE DEL FILE XML CON race_name race_date email
        # leggere le specifiche ed individuare quali parametri potrebbero essere aggiunti e inserirli nell'if sopra
        
    else:
        response['Body'] = 'Error 404: resource not found'
        
    return response