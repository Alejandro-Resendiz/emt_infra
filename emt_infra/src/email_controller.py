import boto3
import json
import logging
import os
from botocore.exceptions import ClientError
from src.utils import (
    EmtJsonEncoder,
    get_response_headers
)

CHAR_SET = "UTF-8"
PINPOINT_APP_ID = os.getenv(
    "EMT_PINPOINT_APP_ID", None
)

logger = logging.getLogger(__name__)
pinpoint_client = boto3.client('pinpoint')


# Functions used to perform the CR operations regarding `campaign`
def do_create(event):
    try:
        payload = json.loads(event.get('body', "{}"))
        email_from = payload['from']
        email_to_addresses = payload['to']
        email_subject = payload['subject']
        email_body = payload['body']
        file_url = payload['file_url'] 

        response = pinpoint_client.send_messages(
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
                            # TODO: Fix File URL. Currently building html part on Frontend
                            # "HtmlPart": {"Charset": CHAR_SET, "Data": """"<html><head><\/head><body>><p>Your file is <a href='{file_url}'>Here<\/a>.<\/p><\/body><\/html>\""""},
                            "HtmlPart": {"Charset": CHAR_SET, "Data": email_body}
                            # "TextPart": {"Charset": CHAR_SET, "Data": email_body}
                        },
                    }
                },
            }
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
            "body": json.dumps(
                {"data": response["MessageResponse"]["Result"]},
                cls=EmtJsonEncoder
            )
        }


def query_get(event):
    try:
        click_response = pinpoint_client.get_application_date_range_kpi(
            ApplicationId=PINPOINT_APP_ID,
            KpiName="txn-emails-clicked"
        )
        delivered_response = pinpoint_client.get_application_date_range_kpi(
            ApplicationId=PINPOINT_APP_ID,
            KpiName="txn-emails-delivered"
        )
        open_response = pinpoint_client.get_application_date_range_kpi(
            ApplicationId=PINPOINT_APP_ID,
            KpiName="txn-emails-opened"
        )
        sent_response = pinpoint_client.get_application_date_range_kpi(
            ApplicationId=PINPOINT_APP_ID,
            KpiName="txn-emails-sent"
        )
        spam_response = pinpoint_client.get_application_date_range_kpi(
            ApplicationId=PINPOINT_APP_ID,
            KpiName="txn-emails-complaint-rate"
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
            "body": json.dumps(
                {"data": {
                    "clicked": click_response["ApplicationDateRangeKpiResponse"]["KpiResult"],
                    "delivered": delivered_response["ApplicationDateRangeKpiResponse"]["KpiResult"],
                    "opened": open_response["ApplicationDateRangeKpiResponse"]["KpiResult"],
                    "sent": sent_response["ApplicationDateRangeKpiResponse"]["KpiResult"],
                    "spam": spam_response["ApplicationDateRangeKpiResponse"]["KpiResult"]
                }},
                cls=EmtJsonEncoder
            )
        }
