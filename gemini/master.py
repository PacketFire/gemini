from flask import Flask
import metadata

app = Flask('gemini-master')


@app.route('/')
def home() -> str:
    return "Home"

@app.route('/_info')
    metadata._info()

def start_master_server() -> None:
    app.run(debug=True)
