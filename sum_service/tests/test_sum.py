from main import random_sum


def test_sum():
    out = random_sum(5, 5)
    assert out == 10
