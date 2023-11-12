from config import ENV_URL
from requests import get


def test_sum():
    resp = get(f"{ENV_URL}/sum", {'num': 2})
    assert "ans" in resp.json(), resp.json()
