from flask import Flask
import json
import metadata

app = Flask('gemini-master')


@app.route('/')
def home() -> str:
    return "Home"

@app.route('/_info')
    response = {
        "statusCode": 200,
        "body": json.dumps(metadata.version())
    }
    return response

def start_master_server() -> None:
    app.run(debug=True)
