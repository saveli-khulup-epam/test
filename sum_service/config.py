from dataclasses import dataclass
from argparse import ArgumentParser, Namespace
from os import environ


@dataclass
class Config:
    rn_host: str
    rn_port: int
    host: str
    port: int


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--rn_host", required=True
    )
    parser.add_argument(
        "--rn_port", required=True
    )
    parser.add_argument(
        '--host', default='0.0.0.0'
    )
    parser.add_argument(
        '--port', default='8000'
    )
    return parser.parse_args()


# args = parse_args()
config = None


def set_config():
    return Config(
        rn_host=environ.get('RN_HOST'),
        rn_port=int(environ.get('RN_PORT')),
        host=environ.get('HOST', '0.0.0.0'),
        port=environ.get('PORT', 8000)
    )
