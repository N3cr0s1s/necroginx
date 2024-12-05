import docker
import time

# Initialize Docker client based on the mapped docker.sock
client = docker.DockerClient(base_url='tcp://dind:2375')

try:
    # Start the test container in DinD (Docker-in-Docker)
    print("Starting test container...")
    container = client.containers.run(
        "nginx:latest",
        detach=True,
        ports={'80/tcp': 8080},
        network=""
    )

    # Check: Is the container running?
    max_retries = 10  # Maximum number of retries
    sleep_interval = 1  # Seconds between checks
    for _ in range(max_retries):
        container.reload()  # Refresh the container status
        if container.status == "running":
            print(f"The container is successfully running. IP: {container.attrs['NetworkSettings']['IPAddress']}")
            break
        print(f"Container status: {container.status}. Retrying...")
        time.sleep(sleep_interval)
    else:
        print("Error: The container did not start in time.")
        raise RuntimeError("Container startup failed.")

finally:
    # Cleanup: Stop and remove the container
    print("Stopping and removing the container...")
    container.stop()
    container.remove()
    print("Test completed.")
