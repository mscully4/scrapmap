import os
import json
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEvent


@event_source(data_class=APIGatewayProxyEvent)
def lambda_handler(event, context):
    ## TODO: Cascade deletes
    table_name = os.environ['DYNAMO_TABLE_NAME']

    username = event['requestContext']['authorizer']['claims']['cognito:username']

    table_name = os.environ['DYNAMO_TABLE_NAME']
    destination_id = event.query_string_parameters['destination_id']

    client = boto3.resource('dynamodb')
    table = client.Table(table_name)

    response = table.delete_item(
        Key={
            "PK": username,
            "SK": destination_id + "###DESTINATION"
        }

    )

    return {
        "statusCode": 204
    }
