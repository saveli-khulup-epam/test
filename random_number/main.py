import random

from fastapi import FastAPI

app = FastAPI()


@app.get("/random_number")
def get_random_number():
    return {
        "number": random.randint(0, 100)
    }
