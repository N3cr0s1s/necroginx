FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y nginx

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD python main.py
