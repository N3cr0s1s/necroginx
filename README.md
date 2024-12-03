NecroGinx
=========

**NecroGinx** is a Python-based tool designed to dynamically manage Nginx configurations for Docker containers. It listens for Docker container events (start and stop) and adjusts the Nginx reverse proxy configuration accordingly, enabling automatic routing for exposed services.

Features
--------

*   **Dynamic Routing**: Automatically configures routes for Docker containers based on environment variables.
*   **Nginx Integration**: Manages Nginx configuration and reloads the server as needed.
*   **Event-driven**: Listens for Docker events and responds to container lifecycle changes in real-time.
*   **Validation**: Ensures containers meet necessary conditions (shared network, valid environment variables) before routing.

Requirements
------------

*   Docker (with access to the Docker socket)

NecroGinx is designed to run inside a Docker container and requires no additional installation on the host system.

Installation
------------

1.  Clone the repository:

    ```bash
    git clone https://github.com/N3cr0s1s/necroginx.git
    cd necroginx
    ```

2.  Build and run the Docker container:

    ```bash
    docker build -t necroginx .
    docker run -v /var/run/docker.sock:/var/run/docker.sock -v /etc/nginx/conf.d:/etc/nginx/conf.d necroginx
    ```


Usage
-----

### Environment Variables

NecroGinx relies on specific environment variables in the Docker containers to configure routing:

*   **`NECROGINX_ROUTE`**: Specifies the route name for the container.
*   **`NECROGINX_PORT`**: Specifies the port number to be exposed.

### Behavior

1.  **On Container Start**:

    *   Validates if the container is on the same network as NecroGinx.
    *   Checks for the presence of required environment variables (`NECROGINX_ROUTE`, `NECROGINX_PORT`).
    *   Generates an Nginx configuration for the container and reloads Nginx.
2.  **On Container Stop**:

    *   Removes the Nginx configuration for the stopped container.
    *   Reloads Nginx.

### Example Workflow

1.  Start a container with the required environment variables:

    ```bash
    docker run -d \
    --network my-network \
    -e NECROGINX_ROUTE=my-service \
    -e NECROGINX_PORT=8080 \
    my-docker-image
    ```

    **Note**: The container and NecroGinx must share at least one network.

2.  NecroGinx automatically detects the container, configures Nginx, and exposes the service at `/my-service`.

3.  Stop the container:

    ```bash
    docker stop <container_id>
    ```

    NecroGinx removes the configuration and reloads Nginx.


Configuration Details
---------------------

### Generated Nginx Config

For a container with:

*   Route: `my-service`
*   Host: `container-hostname`
*   Port: `8080`

The following Nginx configuration is generated:

```nginx
location /my-service {
    if ($uri = "/my-service") {
        rewrite ^ / break;
    }

    rewrite ^/my-service(/.*)?$ $1 break;
    proxy_pass http://container-hostname:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Connection "upgrade";
    proxy_set_header Upgrade $http_upgrade;
}
```

Contributing
------------

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bugfix.
3.  Commit your changes and open a pull request.

Contact
-------

For issues or suggestions, feel free to open an issue on the [GitHub repository](https://github.com/N3cr0s1s/necroginx).

* * *

Automate your container routing effortlessly with **NecroGinx**! 🚀