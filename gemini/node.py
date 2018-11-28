import asyncio, time, requests

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
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, headers)

    print(r.json())