import base64
import boto3
import json
import logging
import os
from botocore.exceptions import ClientError
from src.utils import get_response_headers

S3_BUCKET_NAME = os.getenv(
    "EMT_S3_BUCKET_NAME", None
)

logger = logging.getLogger(__name__)
s3_client = boto3.client('s3')


def do_create(event):
    try:
        file_name = event['queryStringParameters']['filename']
        # TODO: figure out why query param is repeated
        file_name = file_name.split(",")[0] if "," in file_name else file_name
        file_content = event["body"]
        decoded_file = base64.b64decode(file_content)

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME, 
            Key=file_name, 
            Body=decoded_file
        )
        bucket_location = s3_client.get_bucket_location(
            Bucket=S3_BUCKET_NAME
        )

        file_url = f'''https://s3-{
            bucket_location['LocationConstraint']
        }.amazonaws.com/{S3_BUCKET_NAME}/{file_name}'''
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
            "body": json.dumps({
                "data": file_url
            })
        }


def do_delete(event):
    try:
        file_name = event['pathParameters']['key']
        

        s3_client.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name
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
            "body": json.dumps({
                "data": "File deleted successfully"
            })
        }
