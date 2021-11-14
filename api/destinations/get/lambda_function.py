import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEvent

class ItemEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(ItemEncoder, self).default(o)


def query_table(table_name, key=None, value=None):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)

    if key is not None and value is not None:
        filtering_exp = Key(key).eq(value)
        return table.query(KeyConditionExpression=filtering_exp)

    raise ValueError('Parameters missing or invalid')

@event_source(data_class=APIGatewayProxyEvent)
def lambda_handler(event, context):
    table_name = os.environ['DYNAMO_TABLE_NAME']
    user = event.query_string_parameters['user']

    res = query_table(table_name, key="PK", value=user)
    
    return {
        "statusCode": 200,
        "body": json.dumps(res['Items'], cls=ItemEncoder)
    }