FROM python:3.11

COPY requirements.txt .
COPY main.py .
COPY config.py .

RUN python3 -m venv venv && \
    chmod 777 venv/bin/activate && \
    ./venv/bin/activate && \
    pip3 install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "127.0.0.1"]