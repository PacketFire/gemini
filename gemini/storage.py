import consul
from abc import ABC
from abc import abstractmethod
from typing import Any
from mypy_extensions import TypedDict
import json
import functools

c = consul.Consul(host='127.0.0.1', port=8500)

node = TypedDict('node', {'node_id': str, 'password': str})


class NodeInfoRepository(ABC):
    def __init__(self):
        self.node_data = {}
        super().__init__()

    @abstractmethod
    def put_node(self, value: dict):
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> node:
        pass

    @abstractmethod
    def get_all_nodes(self) -> dict:
        pass


class MemoryNodeInfoRepository(NodeInfoRepository):
    def __init__(self):
        self.node_data = {}

    def put_node(self, value: dict):
        self.node_data[value['node_id']] = value

    def get_node(self, node_id: str) -> node:
        return self.node_data[node_id]

    def get_all_nodes(self) -> dict:
        return self.node_data


class ConsulNodeInfoRepository(NodeInfoRepository):
    def __init__(self):
        self.node_data = {}

    def put_node(self, value: dict):
        c.kv.put('nodes/' + value['node_id'], json.dumps(value))

    def get_node(self, node_id: str) -> node:
        self.node_data = c.kv.get('nodes/' + node_id)

        if all(self.node_data):
            output = json.loads(self.node_data[1]['Value'])

        return output


    def get_all_nodes(self) -> dict:
        self.node_data = c.kv.get('nodes/')

        if all (self.node_data):
            output = json.loads(self.node_data)

        return output


@functools.lru_cache(maxsize=None)
def determine_store(store) -> NodeInfoRepository:
    ds: Any
    if store == 0:
        ds = MemoryNodeInfoRepository()
    else:
        ds = ConsulNodeInfoRepository()

    return ds
