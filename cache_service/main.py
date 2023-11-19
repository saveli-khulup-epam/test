import time
from typing import Any

from fastapi import FastAPI

app = FastAPI()

cache: dict[str, tuple[int, Any]] = {}


@app.get('/get')
def get_value(key: str):
    ts, value = cache.get(key, (0, None))
    if value is None or ts < time.time():
        cache.pop(key, None)
        return {
            'value': None
        }
    return {
        'value': value
    }


@app.post('/set', status_code=201)
def set_value(key: str, value: Any, timeout_s: int):
    cache[key] = (int(time.time()) + timeout_s, value)
