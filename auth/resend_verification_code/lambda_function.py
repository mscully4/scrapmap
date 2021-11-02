import json
import boto3
import hmac
import hashlib as hl
import base64
import os

import json
import boto3
import botocore.exceptions
import hmac
import hashlib as hl
import base64
import uuid

def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hl.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def lambda_handler(event, context):
    #Validate Environment Variables
    for env_var in ("CLIENT_ID", "CLIENT_SECRET"):
        if env_var not in os.environ:
            raise KeyError(f"Environemnt varibale {env_var} does not exist")

    #Retrieve secrets stored as environment variables
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ["CLIENT_SECRET"]
    
    body = json.loads(event['body'])

    #Validate body
    missing_fields = []
    for field in ["username"]:
        if field not in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": f"Missing fields: " + ",".join(missing_fields)
        }

    username = body['username']

    try:
        client = boto3.client('cognito-idp')
        secret_hash = get_secret_hash(username, client_id, client_secret)

        response = client.resend_confirmation_code(
            ClientId=client_id,
            SecretHash=secret_hash,
            Username=username,
        )
    
    except client.exceptions.UserNotFoundException:
        return {
            "statusCode": 404, 
            "body": "User does not exist"
        }
        
    except client.exceptions.InvalidParameterException:
        return {
            "statusCode": 400, 
            "body": "User is already confirmed"
        }
    
    except Exception as e:
        return {
            "statusCode": 500, 
            "body": "Error. Please try again later"
        }
    
    finally:
      
        return {
            "statusCode": 204
        }
