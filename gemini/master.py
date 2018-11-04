from flask import Flask
import json

VERSION = "0.1"
app = Flask('gemini-master')


@app.route('/')
def home() -> str:
    return "Home"

@app.route('/_info')
def info() -> str:
    body = {
        "version":  VERSION 
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def start_master_server() -> None:
    app.run(debug=True)
