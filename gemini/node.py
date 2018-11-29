import asyncio, time, requests, json

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
        nd = Nodedata(node_id, password)

        write_node_file(nd)

        print(response['token'])
    except ValueError:
        print('no token returned, credentials do not validate.')


def read_node_file() -> Nodedata:
    try:
        with open('data/node.json', 'r') as fh:
            data = json.load(fh)
            return Nodedata(data['node_id'], data['password'])
    except IOError:
        # for now return blank data on error
        return Nodedata('', '')


def write_node_file(data: Nodedata):
    filedata = {
        'node_id': data.get_node_id(),
        'password': data.get_node_password(),
    }
    try:
        with open('data/node.json', 'r') as fh:
            fh.write(json.dumps(filedata))
    except IOError:
        with open('data/node.json', 'w') as fh:
            fh.write(json.dumps(filedata))


def node_file_exists() -> bool:
    try:
        fh = open('data/node.json', 'r')
        fh.close()
        return True
    except IOError:
        return False
