from flask import Flask


app = Flask('gemini-master')


@app.route('/')
def home() -> str:
    return "Home"


def start_master_server() -> None:
    app.run(debug=True)
