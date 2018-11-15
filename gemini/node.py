import sched, time, requests

def start_node() -> None:
    print('starting node')
    sched_handler()

def ping_master() -> str:
    r = requests.post("http://localhost:5000/v1/nodes/ping")

    return r.status_code

def sched_handler() -> None:
    s = sched.scheduler(time.time, time.sleep)

    s.enter(30, 1, ping_master())