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
    for env_var in ("CLIENT_ID", "CLIENT_SECRET"):
        if env_var not in os.environ:
            raise KeyError(f"Environemnt varibale {env_var} does not exist")
    
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ["CLIENT_SECRET"]
    client = boto3.client('cognito-idp')

    body = json.loads(event['body'])

    #Validate request body
    missing_fields = []
    for field in ["username", "challenge_name", "challenge_responses", "session"]:
        if field not in event:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": "Missing fields: " + ",".join(missing_fields)
        }

    username = body['username']
    challenge_name = body['challenge_name']
    challenge_responses = body['challenge_responses']
    session = body['session']

    try:
        client = boto3.client('cognito-idp')

        secret_hash = get_secret_hash(username, client_id, client_secret)
        challenge_responses['SECRET_HASH'] = secret_hash

        resp = client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName=challenge_name,
            Session=session,
            ChallengeResponses=challenge_responses
        )

    except client.exceptions.NotAuthorizedException as e:
        return {
            "statusCode": 401, 
            "body": "Invalid Request"
        }

    except client.exceptions.UserNotConfirmedException:
        return {
            "statusCode": 403,
            "body": "User is not confirmed"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Error.  Please try again later."
        }

    return {
        "statusCode": 200,
        "body": json.dumps(resp)
    }