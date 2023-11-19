from fastapi import FastAPI
from starlette.requests import Request

from config import config, set_config
from uvicorn import run
from requests import get, post
from multiprocessing import Process

app = FastAPI()
processes: list[Process] = []


def random_sum(rand, num):
    return rand + num


def generate_load(x):
    while True:
        x * x


@app.get('/generate')
def load(x: int):
    processes.append(
        Process(target=generate_load, args=(x,))
    )
    processes[-1].start()


@app.get('/stop_load')
def stop_load():
    for process in processes:
        process.kill()
    processes.clear()


def generate_response_sum(num, random_num):
    return {
        "ans": num + random_num,
        "random_num": random_num,
        'version': 70
    }


@app.get('/sum')
def sum_get(num: int, request: Request):
    client_ip = request.client.host
    key = f"{client_ip}:{num}"
    cache_rand = get(f"{cache_url}/get", params={'key': key}).json().get('value')
    if cache_rand:
        return generate_response_sum(
            num, cache_rand
        )

    try:
        random_num = get(f"{rn_url}/random_number").json()['number']
        post(
            f"{cache_url}/set", params={'key': key, 'value': random_num, 'timeout': 5}
        )
        return generate_response_sum(
            num, random_num
        )
    except Exception as err:
        return {
            "error": str(err),
            "rn": f"{config.rn_host}:{config.rn_port}"
        }


if __name__ == '__main__':
    config = set_config()
    rn_url = f"http://{config.rn_host}:{config.rn_port}"
    cache_url = f"http://{config.cache_host}:{config.cache_port}"
    run(
        app,
        host=config.host,
        port=config.port
    )
