import logging
import constants
import docker
import container_utils
import container_handler
import nginx_handler
from docker.errors import DockerException

def start():
    logging.info(f"{constants.PROGRAM_NAME} Started...")

    nginx_handler.start_nginx_server()

    # Connect to the Docker socket
    try:
        client = docker.DockerClient(base_url=constants.DOCKER_API_URL)
        logging.info("Docker client connected")
    except DockerException as e:
        logging.error("Docker not running, or missing mapping")
        return -1

    # Check is the program running in a container
    try:
        my_container = container_utils.get_my_container(client)
        logging.info(f"My container: {my_container}")
        for network_name, network_details in container_utils.get_container_networks(my_container).items():
            logging.info(f"- {network_name} (IP: {network_details['IPAddress']})")
        logging.info("-" * 30)
    except DockerException as e:
        logging.error("This program only can run in docker container")
        return -1

    logging.info("Listening for Docker events...")
    try:
        # Listen to Docker events
        for event in client.events(decode=True):
            # Filter for container start and stop events
            if event.get("Type") == "container":
                status = event.get("Action")
                container_id = event.get("id")

                container = client.containers.get(container_id)
                if status in ["start"]:
                    container_handler.container_started(client, container)
                if status in ["stop"]:
                    container_handler.container_stopped(container)

    except KeyboardInterrupt:
        logging.info("Stopping listener...")
    finally:
        client.close()
        logging.info("Stopped listener.")