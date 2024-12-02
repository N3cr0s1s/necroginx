import logging
import subprocess

def start_nginx_server():
    logging.info("Starting nginx server...")
    subprocess.run(["service","nginx","start"])

def reload_nginx_server():
    logging.info("Reloading nginx server...")
    subprocess.run(["service","nginx","reload"])

def stop_nginx_server():
    logging.info("Stopping nginx server...")
    subprocess.run(["service","nginx","stop"])

def is_running() -> bool:
    logging.info("Checking if nginx server is running...")
    return subprocess.run(["service","nginx","status"]).returncode == 0