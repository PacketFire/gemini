import json
import secrets
from typing import Any
from typing import List

import bcrypt
import consul
import metadata
from flask import Flask
from flask import jsonify
from flask import request


NODE_ID_BYTES = 8
NODE_TOKEN_BYTES = 32
NODE_PASSWORD_BYTES = 32

STORAGE_TYPE = "memory"

app = Flask('gemini-master')

c = consul.Consul(host='127.0.0.1', port=8500)

jobs: List[Any] = []


class MemoryNodeInfoRepository:
    def __init__(self):
        self.node_data = {}

    def put_data(self, value: dict):
        self.node_data[value['node_id']] = value

    def get_data(self, node_id: str) -> dict:
        return self.node_data[node_id]


class ConsulNodeInfoRepository:
    def __init__(self):
        self.node_data = {}

    def put_data(self, value: dict):
        c.kv.put('nodes/' + value['node_id'], json.dumps(value))

    def get_data(self, node_id: str) -> dict:
        self.node_data = c.kv.get('nodes/' + node_id)

        if all(self.node_data):
            output = json.loads(self.node_data[1]['Value'])

        return output


ds: Any

if STORAGE_TYPE == "memory":
    ds = MemoryNodeInfoRepository()
else:
    ds = ConsulNodeInfoRepository()


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
    ds.put_data(value)

    response = {
        'node_id': node_id,
        'password': password,
    }

    return jsonify(response)


@app.route('/v1/nodes/auth', methods=['POST'])
def auth() -> str:
    body = request.get_json()
    node_data = ds.get_data(body['node_id'])

    if bcrypt.checkpw(
        body['password'].encode('utf8'),
        node_data['password'].encode('utf8'),
    ):
        token = generate_node_token()
        response = {
            'token': token,
        }
        return jsonify(response)
    else:
        return "Passwords do not match\n"


@app.route('/v1/jobs', methods=['POST'])
def create_job() -> str:
    body = request.get_json()

    global jobs
    jobs.append({
        'image': body['image'],
        'command': body['command'],
    })

    return jsonify(body)


@app.route('/v1/jobs', methods=['GET'])
def get_jobs() -> str:
    return jsonify(jobs)


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
