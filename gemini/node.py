import asyncio, time, requests

def start_node() -> None:
    print('starting node')

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(ping_process())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

async def ping_process() -> None:
    while True:
        await asyncio.sleep(30)
        r = requests.post("http://localhost:5000/v1/nodes/ping")
