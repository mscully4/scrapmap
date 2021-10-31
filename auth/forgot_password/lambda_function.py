import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import os
import hashlib as hl

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

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ["CLIENT_SECRET"]

    body = json.loads(event['body'])

    #Validate request data
    missing_fields = []
    for field in ["username"]:
        if not field in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": f"Missing fields: {missing_fields}"
        }

    username = body['username']

    try:
        client = boto3.client('cognito-idp')

        response = client.forgot_password(
            ClientId=client_id,
            SecretHash=get_secret_hash(username, client_id, client_secret),
            Username=username,
        )

    except client.exceptions.UserNotFoundException:
        return {
            "statusCode": 404,
            "body": "User doesn't exist"
        }

    except client.exceptions.InvalidParameterException:
        return {
            "statusCode": 400, 
            "body": f"User <{username}> is not confirmed yet"
        }
    
    except client.exceptions.CodeMismatchException:
        return {
            "statusCode": 400, 
            "body": "Invalid verification code"
        }
    
    except client.exceptions.NotAuthorizedException:
        return {
            "statusCode": 403,
            "body": "Not authorized"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Please try again later"
        }
     
    return {
        "statusCode": 204
    }
