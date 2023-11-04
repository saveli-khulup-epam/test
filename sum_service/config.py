from dataclasses import dataclass
from argparse import ArgumentParser, Namespace


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
    rn_host=args.rn_host,
    rn_port=args.rn_port,
    host=args.host,
    port=int(args.port)
)
