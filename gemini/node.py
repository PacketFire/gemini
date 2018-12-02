import asyncio
import json
from typing import Any
from typing import List
from typing import NamedTuple
from typing import Optional

import docker
import requests


jobs: List[Any]


class NodeData(NamedTuple):
    node_id: str
    password: str


def read_node_file() -> NodeData:
    try:
        with open('data/node.json', 'r') as fh:
            data = json.load(fh)
            return NodeData(data['node_id'], data['password'])
    except IOError:
        # for now return blank data on error
        return NodeData('', '')


def write_node_file(node_data: NodeData) -> None:
    file_data = {
        'node_id': node_data.node_id,
        'password': node_data.password,
    }

    try:
        with open('data/node.json', 'r') as fh:
            fh.write(json.dumps(file_data))
    except IOError:
        with open('data/node.json', 'w') as fh:
            fh.write(json.dumps(file_data))


def node_file_exists() -> bool:
    try:
        fh = open('data/node.json', 'r')
        fh.close()
        return True
    except IOError:
        return False


def start_node() -> None:
    print('Checking if node data exists...')
    if node_file_exists():
        print('Found node data.')

        node_data = read_node_file()
        if authenticate(node_data.node_id, node_data.password) is True:
            get_jobs()
            run_jobs()
            ping_loop()
    else:
        print('Node data not found.')

        new_data = join()
        if new_data is None:
            pass
        else:
            if authenticate(new_data.node_id, new_data.password,) is True:
                get_jobs()
                run_jobs()
                ping_loop()


async def ping() -> None:
    url = 'http://localhost:5000/v1/nodes/ping'
    headers = {'Authorization': 'dummy'}

    while True:
        await asyncio.sleep(30)
        requests.post(url, headers=headers)


def join() -> Optional[NodeData]:
    print('Joining master.')

    url = 'http://localhost:5000/v1/nodes/join'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers)

    try:
        body = response.json()
        node_data = NodeData(body['node_id'], body['password'])

        print('Joined master. Assigned node ID ' + node_data.node_id)

        write_node_file(node_data)

        return node_data
    except ValueError:
        print('Failed to join master.')

        return None


def authenticate(node_id, password) -> bool:
    print('Authenticating with master.')

    url = 'http://localhost:5000/v1/nodes/auth'
    headers = {'Content-Type': 'application/json'}

    payload = {
        'node_id': node_id,
        'password': password,
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        body = response.json()
        print('Successfully authenticated with master: ' + body['token'])
        return True
    except ValueError:
        print('Invalid node credentials.')

        return False


def ping_loop():
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(ping())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


def run_docker_container(image, command):
    client = docker.from_env()
    client.containers.run(image, command)


def get_jobs():
    global jobs

    url = 'http://localhost:5000/v1/jobs'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)
    jobs = response.json()
    print(jobs)


def run_jobs():
    for i in range(len(jobs)):
        run_docker_container(jobs[i]['image'], jobs[i]['command'])
