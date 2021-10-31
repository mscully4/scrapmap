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
    body = json.loads(event['body'])

    missing_fields = []
    for field in ["access_token", "previous_password", "proposed_password"]:
        if field not in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": f"Missing fields: {missing_fields}"
        }

    access_token = body['access_token']
    previous_password = body['previous_password']
    proposed_password = body['proposed_password']

    try:
        client = boto3.client('cognito-idp')

        resp = client.change_password(
            AccessToken=access_token,
            PreviousPassword=previous_password,
            ProposedPassword=proposed_password
        )

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Please try again later"
        }

    return {
        "statusCode": 204
    }