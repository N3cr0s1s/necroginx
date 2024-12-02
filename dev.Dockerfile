FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y nginx procps inotify-tools

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/watcher.sh

CMD ["/app/watcher.sh"]