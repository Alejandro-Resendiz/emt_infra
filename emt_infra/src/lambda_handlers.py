import logging
from src.utils import get_response_headers
from src.email_controller import (
    do_create as create_email_handler,
    query_get as get_email_handler,
)
from src.file_controller import (
    do_create as create_file_handler,
    do_delete as delete_file_handler,
)

logger = logging.getLogger(__name__)


def email_handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''
    # method = event["httpMethod"]
    routeKey = event["routeKey"]

    router = {
        'POST /email': create_email_handler,
        'GET /email': get_email_handler,
    }

    # if method == "OPTIONS":
    #     return {
    #         "statusCode": 200,
    #         "headers": get_response_headers(),
    #         "body": None,
    #         "isBase64Encoded": False
    #     }
    # el
    if routeKey in router:
        return router[routeKey](event)
    else:
        error_mesage = f'Unrecognized operation at "{routeKey}"'
        logger.exception(error_mesage)

        return {
            "statusCode": 500,
            "body": error_mesage
        }


def file_handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''
    # method = event["httpMethod"]
    routeKey = event["routeKey"]

    router = {
        'POST /file': create_file_handler,
        'DELETE /file/{key}': delete_file_handler,
    }
    # if method == "OPTIONS":
    #     return {
    #         "statusCode": 200,
    #         "headers": get_response_headers(),
    #         "body": None,
    #         "isBase64Encoded": False
    #     }
    # el
    if routeKey in router:
        return router[routeKey](event)
    else:
        error_mesage = f'Unrecognized operation at "{routeKey}"'
        logger.exception(error_mesage)

        return {
            "statusCode": 500,
            "body": error_mesage
        }
