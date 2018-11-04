import json

VERSION = "v0.0.1"

def _info():
    body = {
        "version":  VERSION
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
