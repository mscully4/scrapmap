import boto3
import botocore.exceptions
import hmac
import hashlib as hl
import base64
import json
import os

def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
        msg=str(msg).encode('utf-8'), digestmod=hl.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def lambda_handler(event, context):
    # Validate Environment Variables
    for env_var in ("CLIENT_ID", "CLIENT_SECRET", "USER_POOL_ID"):
        if env_var not in os.environ:
            raise KeyError(f"Environemnt varibale {env_var} does not exist")
    
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ["CLIENT_SECRET"]
    user_pool_id = os.environ['USER_POOL_ID']

    body = json.loads(event['body'])

    missing_fields = []
    for field in ["username", "confirmation_code", "password"]:
        if field not in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": f"Missing fields: {missing_fields}"
        }

    username = body['username']
    code = body['confirmation_code']
    password = body['password']

    try:
        client = boto3.client('cognito-idp')
        secret_hash = get_secret_hash(username, client_id, client_secret)

        resp = client.confirm_forgot_password(
            ClientId=client_id,
            ConfirmationCode=code,
            Password=password,
            SecretHash=secret_hash,
            Username=username
        )

    except client.exceptions.NotAuthorizedException:
        return {
            "statusCode": 401, 
            "body": "The username or password is incorrect"
        }

    except client.exceptions.UserNotConfirmedException:
        return {
            "statusCode": 403,
            "body": "User is not confirmed"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Please try again later"
        }

    return {
        "statusCode": 204,
    }
