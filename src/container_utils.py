import logging

from docker import DockerClient
from docker.models.containers import Container


def get_my_container(client: DockerClient) -> Container:
    with open('/etc/hostname', 'r') as f:
        container_id = f.read().strip()
        return client.containers.get(container_id)

def get_container_env_vars(container: Container) -> dict[str, str]:
    env_vars = container.attrs['Config']['Env']
    env_dict = {}

    for env_var in env_vars:
        env = env_var.split("=")
        if len(env) == 2:
            env_dict[env[0]] = env[1]

    return env_dict

def get_container_env_value(container: Container, key: str) -> str:
    return get_container_env_vars(container).get(key)

def get_container_network_names(container: Container) -> list[str]:
    networks_dict = get_container_networks(container)
    return list(networks_dict.keys())

def get_common_networks(container1: Container, container2: Container) -> list[str]:
    networks1 = set(get_container_network_names(container1))
    networks2 = set(get_container_network_names(container2))
    logging.debug(f"container1: {networks1}")
    logging.debug(f"container2: {networks2}")
    return list(networks1 & networks2)

def get_container_networks(container: Container) -> dict[str, any]:
    return get_container_network_settings(container)['Networks']

def get_container_ports(container: Container) -> dict[str, list[any]]:
    return get_container_network_settings(container)['Ports']

def get_container_network_settings(container: Container) -> any:
    return container.attrs["NetworkSettings"]

def container_started(container: Container):
    print(f"Container {container.name} started.")
