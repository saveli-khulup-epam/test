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


args = parse_args()
config = Config(
    rn_host=environ.get('RN_HOST', args.rn_host),
    rn_port=environ.get('RN_PORT', args.rn_port),
    host=environ.get('HOST', args.host),
    port=environ.get('PORT', int(args.port))
)
