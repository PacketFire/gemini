import secrets

import consul
import metadata
from flask import Flask
from flask import jsonify

NODE_TOKEN_BYTES = 32

app = Flask('gemini-master')

c = consul.Consul(host='127.0.0.1', port=8500)


@app.route('/')
def home() -> str:
    return "Home"


@app.route('/_info')
def info() -> str:
    response = {
        "version": metadata.version(),
    }
    return jsonify(response)


@app.route('/v1/nodes', methods=['GET'])
def get_nodes() -> str:
    tokens = c.kv.get('nodes/tokens/', keys=True)
    response = tokens[1]

    return jsonify(response)


@app.route('/v1/nodes', methods=['POST'])
def register() -> str:
    node_id = secrets.token_hex(4)
    token = secrets.token_hex(NODE_TOKEN_BYTES)

    c.kv.put(f'nodes/tokens/{token}', node_id)

    response = {
        "token": token,
    }

    return jsonify(response)


def start_master() -> None:
    app.run(debug=True)
