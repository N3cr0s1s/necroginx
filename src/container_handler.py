import logging
import container_utils
import constants
import config_handler
import nginx_handler
from docker import DockerClient
from docker.models.containers import Container

registered_containers = []

def container_stopped(container: Container):
    if not (container.name in registered_containers):
        return

    logging.info(f"Container {container.name} stopped.")
    config_handler.delete_config(container.name)
    nginx_handler.reload_nginx_server()
    registered_containers.remove(container.name)
    logging.info(f"Container {container.name} deleted.")

def container_started(client: DockerClient,container: Container):
    logging.info(f"Container {container.name} started.")
    if not is_valid(client, container):
        logging.info(f"Container {container.name} is not valid.")
        return

    config_handler.create_new_config(get_route(container),container.name,get_port(container))
    nginx_handler.reload_nginx_server()
    registered_containers.append(container.name)

def is_valid(client: DockerClient, started_container: Container):

    # Network check
    my_container = container_utils.get_my_container(client)
    common_networks = container_utils.get_common_networks(started_container, my_container)
    if len(common_networks) < 1:
        logging.info(f"Container {started_container.name} has no common networks with me.")
        return False

    # Route env check
    route_name = get_route(started_container)
    if route_name is None:
        logging.info(f"Container {started_container.name} has no route env name set up.")
        return False

    # Port env check
    port = get_port(started_container)
    if port is None:
        logging.info(f"Container {started_container.name} has no port set up.")
        return False

    return True

def get_route(container: Container) -> str:
    return container_utils.get_container_env_value(container, constants.SLAVE_ROUTE_ENV_NAME)

def get_port(container: Container) -> str:
    return container_utils.get_container_env_value(container, constants.SLAVE_PORT_ENV_NAME)