
import boto3
from dataclasses import dataclass, asdict, fields
import typing
import json
import os
from decimal import Decimal

@dataclass
class Destination:
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
                setattr(self, field.name, field.type(value))

    def serialize(self):
        return {
            "PK": "test",
            "SK": self.destination_id,
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
    body = json.loads(event['body'])

    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    
    try:
        destination = Destination(**body)
        table.put_item(Item=destination.serialize())
    except Exception as e:
        print(e)
    
    return {
        "statusCode": 200
    }