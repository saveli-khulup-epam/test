from dataclasses import dataclass
from argparse import ArgumentParser


@dataclass
class Config:
    rn_host: str
    rn_port: int


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--rn_host", required=True
    )
    parser.add_argument(
        "--rn_port", required=True
    )
    return parser.parse_args()


# config = Config(**parse_args()._asdict())
config = Config(
    rn_host="127.0.0.1",
    rn_port=8000
)