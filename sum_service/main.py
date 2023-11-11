from fastapi import FastAPI
from config import config
from uvicorn import run
from requests import get

app = FastAPI()
rn_url = f"http://{config.rn_host}:{config.rn_port}"


@app.get('/sum')
def sum_get(num: int):
    try:
        random_num = get(f"{rn_url}/random_number").json()['number']
        return {
            "ans": random_num + num,
            "random_num": random_num,
            'version': 1
        }
    except Exception as err:
        return {
            "error": str(err),
            "rn": f"{config.rn_host}:{config.rn_port}"
        }


if __name__ == '__main__':
    run(
        app,
        host=config.host,
        port=config.port
    )
