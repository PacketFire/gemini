import asyncio, time, requests, json

def start_node() -> None:
    print('starting node')
    join_master()

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(ping_process())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


async def ping_process() -> None:
    url = 'http://localhost:5000/v1/nodes/ping'
    headers = {'Authorization': 'dummy'}

    while True:
        await asyncio.sleep(30)
        r = requests.post(url, headers=headers)

def join_master() -> None:
    print('joining master')
    url = 'http://localhost:5000/v1/nodes/join'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers)

    response = r.json()

    print(response['node_id'] + "\n" + response['password'])

    auth_node(response['node_id'], response['password'])


def auth_node(node_id, password) -> None:
    print('authenticating node')
    
    url = 'http://localhost:5000/v1/nodes/auth'
    headers = {'Content-Type': 'application/json'}

    auth = {
        'node_id': node_id,
        'password': password,
    }

    r = requests.post(url, headers=headers, json=auth)

    try:
        response = r.json()
        
        filedata = {
            'node_id': node_id,
            'password': password,
        }
        node_file_writer(filedata)

        print(response['token'])
    except ValueError:
        print('no token returned, credentials do not validate.')


def node_file_reader() -> dict:
    try:
        with open('data/node.json', 'r') as fh:
            data = json.load(fh)
            return data
    except IOError:
        return 'json file does not exist for node'


def node_file_writer(data):
    try:
        with open('data/node.json', 'r') as fh:
            fh.write(json.dumps(data))
    except IOError:
        with open('data/node.json', 'w') as fh:
            fh.write(json.dumps(data))


def node_file_exists() -> bool:
    try:
        fh = open('data/node.json', 'r')
        fh.close()
        return True
    except IOError:
        return False


class Nodedata:
    def __init__(self, node_id, password):
        self.node_id = node_id
        self.password = password

    def get_node_id(self) -> str:
        return self.node_id

    def set_node_id(self, newid):
        self.node_id = newid

    def get_node_password(self) -> str:
        return self.password

    def set_node_password(self, newpass):
        self.password = newpass