
import boto3
from dataclasses import dataclass, asdict, fields
import typing
import json
import os
from decimal import Decimal

@dataclass
class Destination:
    username: str
    destination_id: str
    name: str
    country: str
    country_code: str
    latitude: Decimal
    longitude: Decimal
    destination_type: str #typing.Literal["C", "NP", "NM"]

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                try:
                    setattr(self, field.name, field.type(value))
                except BaseException as e:
                    logger.error(f"{field.name} can't be converted to {field.type}")
                    raise

    def serialize(self):
        return {
            "PK": self.username,
            "SK": f"{self.destination_id}###DESTINATION",
            "Entity": {
                "name": self.name,
                "country": self.country,
                "country_code": self.country_code,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "destination_type": self.destination_type
            }
        }

def lambda_handler(event, context):
    table_name = os.environ['DYNAMO_TABLE_NAME']
    username = event['requestContext']['authorizer']['claims']['cognito:username']

    body = json.loads(event['body'])

    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    
    try:
        destination = Destination(username=username, **body)
        table.put_item(Item=destination.serialize())
    except Exception as e:
        print(e)
    
    return {
        "statusCode": 200
    }