import os
import boto3
from dotenv import load_dotenv, find_dotenv

def getIdToken(user, passw):
    username = user
    password = passw

    load_dotenv(find_dotenv())

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)

    client = boto3.client("cognito-idp", region_name="us-east-1")

    # Initiating the Authentication, 
    response = client.initiate_auth(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
    
    identity_token = response["AuthenticationResult"]["IdToken"]

    return identity_token