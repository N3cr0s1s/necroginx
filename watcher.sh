#!/bin/bash

python_log="/var/log/python_script.log";

# File not exist, creating it
if [ ! -f "$python_log" ]; then
  touch "$python_log"
  echo "File created: $python_log"
fi

# Print python logs
tail -f /var/log/python_script.log &

# Watch and logging
inotifywait -m -e modify --format '%w%f' /app/src | while read file; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') - File changed: $file" >> /var/log/app_watch.log
  echo "Restarting Python script..."

  # Stop already running processes
  pkill -f 'python3 /app/main.py' && echo "Stopped previous instance of main.py" >> /var/log/app_watch.log

  # Restart
  if ! python3 /app/main.py >> /var/log/app_watch.log 2>&1 & then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Failed to restart main.py" >> /var/log/app_watch.log
  fi

  echo "Python script restarted." >> /var/log/app_watch.log
done
