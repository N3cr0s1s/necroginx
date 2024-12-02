import logging

PROGRAM_NAME = "Necroginx"
DOCKER_API_URL = "unix://var/run/docker.sock"

# Slave container parameters
SLAVE_ROUTE_ENV_NAME = "NECROGINX_ROUTE"
SLAVE_PORT_ENV_NAME = "NECROGINX_PORT"

# Logging
LOG_PATH = "/var/log/python_script.log"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = f"[{PROGRAM_NAME}] %(asctime)-15s %(levelname)-8s %(message)s"