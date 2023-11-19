from fastapi import FastAPI
from config import config, set_config
from uvicorn import run
from requests import get
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


@app.get('/sum')
def sum_get(num: int):
    try:
        random_num = get(f"{rn_url}/random_number").json()['number']
        return {
            "ans": random_sum(random_num, num),
            "random_num": random_num,
            'version': 70
        }
    except Exception as err:
        return {
            "error": str(err),
            "rn": f"{config.rn_host}:{config.rn_port}"
        }


if __name__ == '__main__':
    config = set_config()
    rn_url = f"http://{config.rn_host}:{config.rn_port}"
    run(
        app,
        host=config.host,
        port=config.port
    )
