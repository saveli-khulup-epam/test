from config import ENV_URL
from requests import get


def test_random():
    resp = get(f"{ENV_URL}/random_number")
    assert 'number' in resp.json(), resp.json()
