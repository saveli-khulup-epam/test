import os.path
from dataclasses import dataclass

import telebot
from argparse import ArgumentParser

chat_ids = ['953562617']


@dataclass
class ParsedArgs:
    files: list[str]
    job_name: str
    status: str


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--job_name', required=True)
    parser.add_argument('--status', choices=['SUCCESS', 'FAILED', 'SKIPPED'], required=True)

    return parser.parse_args()


parsed = parse_args()
args = ParsedArgs(
    files=parsed.files,
    job_name=parsed.job_name,
    status=parsed.status
)

TELEGRAM_TOKEN = "<token>"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

for chat_id in chat_ids:
    bot.send_message(
        chat_id, f'Job *{args.job_name}* is executed with *{args.status}*.\n'
                 f'{"Artifacts you can find below." if args.files else "There are no artifacts for this job."}',
        parse_mode='Markdown'
    )
    for file in args.files:
        if os.path.exists(file) and os.path.isfile(file):
            with open(file, 'rb') as to_send:
                bot.send_document(chat_id, to_send)
        else:
            raise RuntimeError(f'File `{file}` doesn\'t exists or it is a folder!')
