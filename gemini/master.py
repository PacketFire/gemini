from flask import Flask
import json
import metadata

app = Flask('gemini-master')


@app.route('/')
def home() -> str:
    return "Home"

@app.route('/_info')
def info() -> str:
    response = {
        "version": json.dumps(metadata.version())
    }
    return str(response)

def start_master_server() -> None:
    app.run(debug=True)
