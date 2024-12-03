FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y nginx procps inotify-tools

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x /app/watcher.sh

CMD ["/app/watcher.sh"]