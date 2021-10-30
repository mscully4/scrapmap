import json
import boto3
import hmac
import hashlib as hl
import base64
import os

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

    #Validate request data
    missing_fields = []
    for field in ["username", "email", "password", "first_name", "last_name", "phone_number"]:
        if field not in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": f"Missing fields: {missing_fields}"
        }

    #Retrieve request data
    username = event['username']
    email = event['email']
    password= event['password']
    given_name = event['first_name']
    last_name = event['last_name']
    phone_number = event['phone_number']

    try:
        #Create Cognito client
        client = boto3.client('cognito-idp')

        resp = client.sign_up(
            ClientId=client_id,
            SecretHash=get_secret_hash(username, client_id, client_secret),
            Username=username,
            Password=password, 
            UserAttributes=[
                {
                    'Name': "email",
                    'Value': email
                },
                {
                    'Name': "given_name",
                    'Value': given_name
                },
                {
                    'Name': 'family_name',
                    'Value': last_name
                },
                {
                    'Name': "phone_number",
                    'Value': phone_number
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                }
            ]
        )

        return {
            "statusCode": 201,
            "body": "User created!  Check your email for a validation code", 
        }

    except client.exceptions.UsernameExistsException as e:
        return {
            "statusCode": 400,
            "body": "An account with this username already exists"
        }

    except client.exceptions.InvalidPasswordException as e:
        return {
            "statusCode": 400,
            "body": "Invalid password. Password should have at least one uppercase letter, one lowercase letter and one number", 
        }

    except client.exceptions.UserLambdaValidationException as e:
        return {
            "statusCode": 400,
            "body": "An account with this email already exists", 
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Error. Please try again later", 
        }
