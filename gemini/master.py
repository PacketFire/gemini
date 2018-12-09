import secrets
from typing import Any
from typing import List

import bcrypt
import metadata
import storage
from flask import Flask
from flask import jsonify
from flask import request


NODE_ID_BYTES = 8
NODE_TOKEN_BYTES = 32
NODE_PASSWORD_BYTES = 32
NODE_STORAGE = 0


app = Flask('gemini-master')

jobs: List[Any] = []

ds = storage.determine_store(NODE_STORAGE)


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
