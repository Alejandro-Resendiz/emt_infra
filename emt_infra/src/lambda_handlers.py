import boto3
import json
import logging
import os
from botocore.exceptions import ClientError

CHAR_SET = "UTF-8"
# TODO - Remove App ID
PINPOINT_APP_ID = os.getenv(
    "EMT_PINPOINT_APP_ID", "84c08d3b84a54b77a984f905762f6911"
)

logger = logging.getLogger(__name__)
pinpoint_client = boto3.client('pinpoint')


def handler_manager(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''
    method = event["httpMethod"]
    operation = event.get('operation', None)

    operations = {
        'create': do_create,
        'get': query_get,
        'get_one': query_get_one,
    }

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": get_response_headers(),
            "body": None,
            "isBase64Encoded": False
        }
    elif operation in operations:
        return operations[operation](event.get('payload'))
    else:
        error_mesage = f'Unrecognized operation "{operation}"'
        logger.exception(error_mesage)

        return {
            "statusCode": 500,
            "body": error_mesage
        }


# Functions used to perform the CR operations regarding `campaign`
def do_create(payload):
    try:
        email_from = payload['from']
        email_to_addresses = payload['to']
        email_subject = payload['subject']
        email_body = payload['body']

        response = pinpoint_client.send_message(
            ApplicationId=PINPOINT_APP_ID,
            MessageRequest={
                "Addresses": {
                    to_address: {"ChannelType": "EMAIL"} for to_address in email_to_addresses
                },
                "MessageConfiguration": {
                    "EmailMessage": {
                        "FromAddress": email_from,
                        "SimpleEmail": {
                            "Subject": {"Charset": CHAR_SET, "Data": email_subject},
                            # "HtmlPart": {"Charset": CHAR_SET, "Data": html_message},
                            "TextPart": {"Charset": CHAR_SET, "Data": email_body},
                        },
                    }
                },
            },)
    except ClientError as e:
        logger.exception(e)

        return {
            "statusCode": 500,
            "body": str(e)
        }
    else:
        return {
            "statusCode": 200,
            "headers": get_response_headers(),
            "body": {
                to_address: message["MessageId"]
                for to_address, message in response["MessageResponse"]["Result"].items()
            }
        }


def query_get(payload):
    try:
        response = pinpoint_client.get_campaigns(
            ApplicationId=PINPOINT_APP_ID,
            PageSize='100'
        )
    except ClientError as e:
        logger.exception(e)

        return {
            "statusCode": 500,
            "body": str(e)
        }
    else:
        return {
            "statusCode": 200,
            "headers": get_response_headers(),
            "body": json.dumps(response)
        }


def query_get_one(x):
    pass
    # dynamo.update_item(**x)


def get_response_headers():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    }
    return headers
