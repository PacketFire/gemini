import json
import secrets
import bcrypt
import consul
import metadata
from flask import Flask
from flask import jsonify
from flask import request

NODE_ID_BYTES = 8
NODE_TOKEN_BYTES = 32
NODE_PASSWORD_BYTES = 32

app = Flask('gemini-master')

c = consul.Consul(host='127.0.0.1', port=8500)


@app.route('/')
def index() -> str:
    return 'index'


@app.route('/_info')
def info() -> str:
    response = {
        'version': metadata.version(),
    }

    return jsonify(response)


@app.route('/v1/nodes/join', methods=['POST'])
def join() -> str:
    node_id = generate_node_id()
    password = generate_node_password()
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    value = {
        'node_id': node_id,
        'password': hashed.decode('utf8'),
    }

    c.kv.put('nodes/' + node_id, json.dumps(value))

    response = {
        'node_id': node_id,
        'password': password,
    }

    return jsonify(response)


@app.route('/v1/nodes/auth', methods=['POST'])
def auth() -> str:
    data = request.get_json()
    cdata = c.kv.get('nodes/' + data['node_id'])
    cvalues = json.loads(cdata[1]['Value'])

    if bcrypt.checkpw(data['password'].encode('utf8'), cvalues['password'].encode('utf8')):
        token = generate_node_token()
        response = {
            'token': token,
        }
        return jsonify(response)
    else:
        return "Passwords do not match\n"


@app.route('/v1/nodes/ping', methods=['POST'])
def ping() -> str:
    token = request.headers.get('Authorization')

    return token


@app.route('/v1/nodes/refresh', methods=['POST'])
def refresh() -> str:
    token = request.headers.get('Authorization')
    new_token = generate_node_token()

    response = {
        'old_token': token,
        'new_token': new_token,
    }

    return jsonify(response)

def generate_node_id() -> str:
    return secrets.token_hex(NODE_ID_BYTES)

def generate_node_token() -> str:
    return secrets.token_hex(NODE_TOKEN_BYTES)

def generate_node_password() -> str:
    return secrets.token_hex(NODE_PASSWORD_BYTES)

def start_master() -> None:
    app.run(debug=True)
