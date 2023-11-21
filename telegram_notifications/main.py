import os.path

import telebot
from fastapi import FastAPI
import requests
from pathlib import Path
import base64

chat_ids = ['953562617']
TELEGRAM_TOKEN = "TELEGRAM TOKEN"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

app = FastAPI()
JENKINS_URL = 'http://192.168.56.105:8080'
JENKINS_TOKEN = '<JENKINS TOKEN>'
HEADERS = {
    'Authorization': f'Basic {base64.b64encode(JENKINS_TOKEN.encode("utf-8")).decode("utf-8")}'
}

ARTIFACTS_PATH = Path('artifacts')


def download_files(job_name: str, job_id: int) -> list[str]:
    if not os.path.isdir(ARTIFACTS_PATH):
        os.mkdir(ARTIFACTS_PATH)
    base_url = f"{JENKINS_URL}/job/{job_name}/{job_id}"
    artifacts = requests.get(f"{base_url}/api/json", headers=HEADERS).json()['artifacts']
    file_names = []
    for artifact in artifacts:
        file_name = artifact['fileName']
        with open(ARTIFACTS_PATH / artifact['fileName'], 'wb') as file:
            content = requests.get(f'{base_url}/artifact/{file_name}', headers=HEADERS).content
            file.write(content)
        file_names.append(ARTIFACTS_PATH / file_name)
    return file_names


def clear_artifacts(file_names: list[str]):
    for file_name in file_names:
        os.remove(file_name)


@app.get('/send_notifications')
def send_notification(job_id: int, job_name: str, status: str):
    files = download_files(job_name, job_id)
    for chat_id in chat_ids:
        bot.send_message(
            chat_id, f'Job *{job_name}* is executed with *{status}*.\n'
                     f'{"Artifacts you can find below." if files else "There are no artifacts for this job."}',
            parse_mode='Markdown'
        )
        for file in files:
            if os.path.exists(file) and os.path.isfile(file):
                with open(file, 'rb') as to_send:
                    bot.send_document(chat_id, to_send)
            else:
                raise RuntimeError(f'File `{file}` doesn\'t exists or it is a folder!')
    clear_artifacts(files)
